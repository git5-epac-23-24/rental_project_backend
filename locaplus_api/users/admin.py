from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User
from .models import Customer, Owner, User
# Register your models here.


class UserInline(admin.StackedInline):
    model = User
    can_delete = False
    verbose_name_plural = "users"
    
    
class OwnerInline(admin.StackedInline):
    model = Owner
    can_delete = False
    verbose_name_plural = "owners"
class UserAdmin(BaseUserAdmin):
    inlines = [OwnerInline]
    
    
# admin.site.unregister(User)
admin.site.register(User, UserAdmin)