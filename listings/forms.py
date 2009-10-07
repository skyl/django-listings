from datetime import datetime
from django import forms

from listings.models import Listing

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        exclude = ('owner', 'state',)



