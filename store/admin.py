from django.contrib import admin
from .models import *

# Register your models here.
class RentAdmin(admin.ModelAdmin):
    list_display=('user', 'product', 'start_date', 'end_date', 'duration', 'cost', 'status')
    list_filter = ('product', 'status', 'start_date', 'end_date')
    search_fields = ("product", "start_date", "end_date")
    ordering = ("product", "start_date")

    fieldsets = (
        (None, {
            'fields': ('user', 'duration', 'cost')
        }),
        ('Availability', {
            'fields': ('product', 'status', 'start_date', 'end_date')
        }),
    )
    
class ProductAdmin(admin.ModelAdmin):
    list_display=('owner', 'name', 'description', 'price', 'stock', 'type', 'created_at', 'updated_at')
    list_filter = ('type', 'created_at', 'updated_at')
    search_fields = ("name", "description")
    ordering = ("name", "created_at")

    fieldsets = (
        (None, {
            'fields': ('owner', 'name', 'description', 'price', 'stock')
        }),
        ('Availability', {
            'fields': ('type', 'extra_spec', 'picture')
        }),
    )
    
# Register your models here.

admin.site.register(ProductType)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rent, RentAdmin)
