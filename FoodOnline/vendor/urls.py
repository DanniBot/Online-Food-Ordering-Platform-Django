from django.urls import path,include
from . import views
from accounts import views as accountViews

urlpatterns=[
    path('',accountViews.vendorDashboard,name='vendor'),
    path('profile/',views.v_profile, name='v_profile'),
    
    path('menu-builder/',views.menu_builder,name='menu_builder'),
    path('menu-builder/category/<int:pk>/',views.fooditems_by_category,name='fooditems_by_category'),

    # category CRUD
    path('menu-builder/category/add/',views.add_cat, name='add_cat'),
    path('menu-builder/category/edit/<int:pk>',views.edit_cat, name='edit_cat'),
    path('menu-builder/category/del/<int:pk>',views.del_cat, name='del_cat'),

    # food CRUD
    path('menu-builder/category/<int:pk>/add-food',views.add_food, name='add_food'),
    path('menu-builder/food/edit-food/<int:pk>',views.edit_food, name='edit_food'),
    path('menu-builder/food/del-food/<int:pk>',views.del_food, name='del_food'),

    #opening hour
    path('opening-hours/',views.opening_hour,name='opening_hour'),
    path('opening-hours/add/',views.add_hours,name='add_hours'),
    path('opening-hours/remove/<int:pk>/',views.remove_hours,name='remove_hours'),

    path('order_detail/<int:order_number>/',views.order_detail,name='vendor_order_detail'),
    path('my_orders/',views.my_orders, name='vendor_my_orders'),
]