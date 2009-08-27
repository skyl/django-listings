from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("listing_new", _("New Listing"),
                _("someone has posted a new listing"), default=2)

        notification.create_notice_type("listing_comment", _("Listing Comment"),
                _("someone has commented on your listing"), default=2)

        notification.create_notice_type("listing_done", _("Listing Done"),
                _("a listing you are watching is no longer alive"), default=2)

        notification.create_notice_type("listing_change", _("Listing Changed"),
                _("a listing you are watching has changed"), default=2)

        notification.create_notice_type("listing_delete", _("Listing Deleted"),
                _("a listing you are watching been deleted"), default=2)

        notification.create_notice_type("listing_watch_start", _("Listing Watched"),
                _("a listing you created has a new watcher"), default=2)

        notification.create_notice_type("listing_watch_stop", _("Listing No Longer Watched"),
                _("a listing you created lost a watcher"), default=2)



    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"
