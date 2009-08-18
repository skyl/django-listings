from django import template

from listings.models import WatchRelation

register = template.Library()


@register.inclusion_tag('listings/tags/add_remove.html')
def listing_add_remove(listing, user):
    try:
        watched = WatchRelation.objects.get(watcher=user, listing=listing)

    except:
        watched = None

    finally:
        return locals()
