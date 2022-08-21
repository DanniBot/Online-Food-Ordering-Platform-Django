from ast import arg
from dataclasses import fields
from django import forms
from . models import User,UserProfile
from .validator import allow_obly_images_validator

class userForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','phone_number','password']

    def clean(self):
        cleaned_data = super(userForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

class userProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(widget=forms.FileInput(attrs={'class':'btn btn-info'}))
    # profile_picture=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_obly_images_validator])
    cover_photo=forms.ImageField(widget=forms.FileInput(attrs={'class':'btn btn-info'}))
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholer':'Start typing...','required':'required'}))
    latitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    longitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model=UserProfile
        fields=['profile_picture', 'cover_photo', 'address','country', 'state', 'city', 'pin_code','latitude', 'longitude']

    # def __init__(self,*args,**kwargs):
    #     super(userProfileForm,self).__init__(*args,**kwargs)
    #     for field in self.fields:
    #         if field =='latitude' or field == 'longitude':
    #             self.fields[field].widget.attrs['readonly']=='readonly'

class userInfoForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','phone_number']