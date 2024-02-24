from django.contrib import admin
from .models import *

# Register your models here.
class RentAdmin(admin.ModelAdmin):
    list_display=('product', 'user', 'start_date', 'end_date', 'duration', 'cost', 'status')
    list_filter = ('product', 'status', 'start_date', 'end_date')
    search_fields = ("product", "start_date", "end_date")
    ordering = ("product", "start_date")

    fieldsets = (
        (None, {
            'fields': ('user', 'duration', 'cost', 'quantity')
        }),
        ('Availability', {
            'fields': ('product', 'status', 'start_date', 'end_date')
        }),
    )
    
class ProductTypeAdmin(admin.ModelAdmin):
    list_display=('name', 'description')
    list_filter = ('name',)
    search_fields = ("name", "description")
    ordering = ("name",)

class ProductAdmin(admin.ModelAdmin):
    list_display=('name', 'description', 'price', 'stock', 'type', 'owner', 'created_at', 'updated_at')
    list_filter = ('name', 'price', 'type', 'owner', 'created_at', 'updated_at')
    search_fields = ("name", "description")
    ordering = ("name", "created_at", "price", "stock")

    # fieldsets = (
    #     (None, {
    #         'fields': ('owner', 'name', 'description', 'price', 'stock')
    #     }),
    #     ('Availability', {
    #         'fields': ('type', 'extra_spec', 'picture')
    #     }),
    # )
    
# Register your models here.

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rent, RentAdmin)
