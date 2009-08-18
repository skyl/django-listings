from django.contrib import admin
from listings.models import Listing

class ListingAdmin(admin.ModelAdmin):
    list_display        = ('owner', 'title', 'description', 'want', 'state',)
    list_filter         = ('owner', 'state')
    search_fields       = ('title', 'description', 'want')

admin.site.register(Listing, ListingAdmin)


