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
    
admin.site.register(Rent, RentAdmin)
