from datetime import datetime

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.template.defaultfilters import slugify

from tagging.fields import TagField
from tagging.models import Tag

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

class Listing(models.Model):
    """ A simple listing for a job

    """

    STATE_CHOICES = (
        (1, _('alive')),
        (2, _('dead')),
        (3, _('completed')),
    )

    owner = models.ForeignKey(User, verbose_name=_('offerer'))
    title = models.CharField(_('short description'), max_length=255)
    slug = models.CharField(editable=False, max_length=255)
    description = models.TextField(_('offering'))
    want = models.TextField(_('want'), blank=True, null=True)
    state = models.PositiveSmallIntegerField(_('state'), max_length="1", choices=STATE_CHOICES, default=1)
    time = models.DateTimeField(_('offered time'), auto_now_add=True)
    tags = TagField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('listings.views.listing', (), {'id':self.id, 'slug':self.slug})
    get_absolute_url = models.permalink(get_absolute_url)

    def is_alive(self):
        """
        """

        if int(self.state) == 1:
            return True
        else:
            return False

    def cancel(self):
        self.state = 2
        self.save()

    def save(self, force_insert=False, force_update=False):
        self.slug = slugify(self.title)
        if self.pk:
            new=False
        else:
            new=True
        super(Listing, self).save(force_insert, force_update)

        if new and notification:
            notification.send(User.objects.all().exclude(id=self.owner.id),
                "listing_new",
                {'listing':self, },
            )

        elif notification and (self.state == 2 or self.state == 3):
            notification.send(User.objects.filter(watchrelation__listing=self).exclude(id=self.owner.id),
                "listing_done",
                {'listing':self, },
            )

        elif notification:
            notification.send(User.objects.filter(watchrelation__listing=self).exclude(id=self.owner.id),
                "listing_change",
                {'listing':self, },
            )

    def delete(self):
        if notification:
            notification.send(User.objects.filter(watchrelation__listing=self).exclude(id=self.owner.id),
                "listing_delete",
                {'listing':self, },
            )
        super(Listing, self).delete()



class WatchRelation(models.Model):
    listing = models.ForeignKey(Listing)
    watcher = models.ForeignKey('auth.User')

    class Meta:
        unique_together = (('listing', 'watcher'),)

# handle notification of new comments
from threadedcomments.models import ThreadedComment
def new_comment(sender, instance, **kwargs):
    if isinstance(instance.content_object, Listing):
        listing = instance.content_object
        if notification:
            commenter = instance.user
            recipient = instance.content_object.owner
            if recipient != commenter:
                notification.send([recipient], "listing_comment",
                        {"commenter": commenter, "listing": listing, "comment": instance})
signals.post_save.connect(new_comment, sender=ThreadedComment)
