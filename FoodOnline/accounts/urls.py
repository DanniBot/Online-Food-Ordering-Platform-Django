from django.urls import path
from . import views

urlpatterns=[
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),

    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('custDashboard/',views.custDashboard,name='custDashboard'),
    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),
    path('myAccount/',views.myAccount,name='myAccount'),
]