from django.urls import path,include
from . import views
from accounts import views as AccountViews

urlpatterns=[
    path('',AccountViews.custDashboard, name='customer'),
    path('profile/',views.c_profile,name='c_profile'),
    
]