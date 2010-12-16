from datetime import datetime
from django import forms

from olwidget.widgets import EditableMap

from listings.models import Listing

class ListingForm(forms.ModelForm):

    location = forms.CharField(widget=EditableMap())

    class Meta:
        model = Listing
        exclude = ('owner', 'state',)



