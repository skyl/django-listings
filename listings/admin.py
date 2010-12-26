from django.contrib import admin
from olwidget.admin import GeoModelAdmin

from listings.models import Listing


class ListingGeoAdmin(GeoModelAdmin):

    list_display        = ('owner', 'title', 'description', 'want', 'state',)
    list_filter         = ('owner', 'state')
    search_fields       = ('title', 'description', 'want')

    list_map = ['location']
    list_map_options = {
        'cluster': True,
        'cluster_display': 'list',
    }

    options = {
        'layers': ['google.streets'],
        'default_lat': 44,
        'default_lon': -72,
    }


admin.site.register(Listing, ListingGeoAdmin)


