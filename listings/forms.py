from django import forms
from .models import Listing, Image


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'quantity', 'category', 'condition']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'alt_text']

