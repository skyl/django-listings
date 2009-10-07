from django.conf.urls.defaults import *

#from listings import views, models
#from listings.forms import ListingForm


urlpatterns = patterns('',

    url(r'^$', 'listings.views.listings', name="listings_all"),

    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        'listings.views.listing', name='listings_detail'),

    url(r'^your_listings/$', 'listings.views.your_listings', name='listings_yours'),

    url(r'watched_listings/$', 'listings.views.watched_listings',
            name='listings_watched'),

    url(r'^create/$', 'listings.views.new', name='listings_new'),

    url(r'^edit/(?P<listing_id>\d+)/$', 'listings.views.edit_listing', name='listings_edit'),

    url(r'^delete/(?P<listing_id>\d+)/$', 'listings.views.delete_listing',
        name='listings_delete'),

    url(r'^watch/(?P<listing_id>\d+)/$', 'listings.views.watch',
        name='listings_watch'),

    # ajax validation
    #(r'^validate/$', 'ajax_validation.views.validate', {'form_class': BlogForm, 'callback': lambda request, *args, **kwargs: {'user': request.user}}, 'blog_form_validate'),
)
