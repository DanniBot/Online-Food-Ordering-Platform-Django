from cgitb import grey
from dataclasses import fields
from unicodedata import category
from django import forms
from .models import Category,foodItem

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['category_name','description']

class foodAddForm(forms.ModelForm):
    class Meta:
        model=foodItem
        fields=['food_name','description','price','image','is_available']

class foodEditForm(forms.ModelForm):
    class Meta:
        model=foodItem
        fields=['food_name','description','category','price','image','is_available']
