from datetime import datetime
from django import forms

from olwidget.widgets import EditableMap

from listings.models import Listing

from geolistings.views import default_map_options

class ListingForm(forms.ModelForm):

    location = forms.CharField(widget=EditableMap(default_map_options))

    class Meta:
        model = Listing
        exclude = ('owner', 'state',)



