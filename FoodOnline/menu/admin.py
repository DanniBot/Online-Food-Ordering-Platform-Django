from django.contrib import admin
from .models import foodItem,Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=('category_name','vendor')
    search_fields=('category_name','vendor__vendor_name')

class foodItemAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('food_name',)}
    search_fields=('food_name','category__category_name','vendor__vendor_name','price')
    list_filter=('is_available',)
    list_display=('food_name','vendor','price','is_available','updated_at')

admin.site.register(Category,CategoryAdmin)
admin.site.register(foodItem,foodItemAdmin)
