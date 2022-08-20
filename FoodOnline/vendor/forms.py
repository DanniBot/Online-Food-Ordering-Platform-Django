from dataclasses import fields
from django import forms
from .models import Vendor,OpeningHour
from accounts.validator import allow_obly_images_validator

class vendorForm(forms.ModelForm):
    vendor_license=forms.ImageField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_obly_images_validator])
    class Meta:
        model=Vendor
        fields=['vendor_name','vendor_license']

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']
