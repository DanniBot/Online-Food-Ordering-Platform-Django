from django.contrib import admin
from .models import Cart,Tax
# Register your models here.

class cartAdmin(admin.ModelAdmin):
    list_display=('user','fooditem','quantity','updated_at')

class taxAdmin(admin.ModelAdmin):
    list_display=('tax_type','tax_percentage','is_active')

admin.site.register(Cart,cartAdmin)
admin.site.register(Tax,taxAdmin)