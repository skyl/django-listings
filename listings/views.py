from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import date_based
from django.conf import settings
from django.db.models import Q
from django.conf import settings

from django.views.generic.create_update import create_object, update_object,\
        delete_object

from listings.models import Listing, WatchRelation
from listings.forms import ListingForm

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

try:
    from threadedcomments.models import ThreadedComment
    forums = True
except ImportError:
    forums = False

def listings(request):
    listings = Listing.objects.filter(state=1).order_by("-time")
    return render_to_response("listings/listings.html", {"listings": listings}, context_instance=RequestContext(request))



def listing(request, id, slug):
    listing = get_object_or_404(Listing, id=id)

    return render_to_response("listings/listing.html", {
        "listing": listing,
    }, context_instance=RequestContext(request))

@login_required
def your_listings(request):
    user = request.user
    listings = Listing.objects.filter(owner=user).order_by("-time")
    is_me=True
    context = locals()
    return render_to_response("listings/your_listings.html",
            context, context_instance=RequestContext(request))

@login_required
def watched_listings(request):
    user = request.user
    listings = Listing.objects.filter(watchrelation__watcher=user)
    context = {'listings':listings, }
    return render_to_response("listings/your_listings.html",
            context, context_instance=RequestContext(request))



@login_required
def new(request):
    ''' Create a new listing with request.user as owner
    '''
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid:
            l = form.save(commit=False)
            l.owner = request.user
            l.save()
            return HttpResponseRedirect(reverse('listings_all'))

    else:
        form = ListingForm()

    return create_object(
            request,
            form_class = ListingForm
    )

@login_required
def edit_listing(request, listing_id):


    return update_object(
            request,
            model=Listing,
            object_id = listing_id,
            extra_context = locals()
    )

@login_required
def delete_listing(request, listing_id):
    '''
    '''
    return delete_object(
        request,
        model = Listing,
        object_id = listing_id,
        post_delete_redirect = reverse('listings_all')
    )

@login_required
def watch(request, listing_id):
    ''' takes a POST and makes a watcher of the request.user

    '''
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == 'POST':
        if request.POST["action"] == "watch":
            w, created = WatchRelation.objects.get_or_create(
                watcher=request.user,
                listing=listing
            )
            notification.send([listing.owner], "listing_watch_start",{
                "listing":listing,
                "watcher":w.watcher,}
            )

        elif request.POST["action"] == "stop":
            w = WatchRelation.objects.get(listing=listing,
                    watcher=request.user)
            w.delete()
            notification.send([listing.owner], "listing_watch_stop",{
                "listing":listing,
                "watcher":w.watcher,}
            )
        return HttpResponseRedirect(reverse('listings_all'))

    else:
        return HttpResponseRedirect(reverse('listings_all'))




