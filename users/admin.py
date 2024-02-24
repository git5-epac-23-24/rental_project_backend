from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from django.contrib.auth.models import User
from .models import User, Role, Subscribers, Email

# Register your models here.


# class UserInline(admin.StackedInline):
#     model = User
#     can_delete = False
#     verbose_name_plural = "users"


class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "phone", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name", "phone")
    ordering = ("username",)
    filter_horizontal = ()
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "phone",
                    "profil_picture",
                    "address",
                    "city",
                    "country",
                    "id_card",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "phone",
                    "profil_picture",
                    "address",
                    "city",
                    "country",
                    "id_card",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Subscribers)
admin.site.register(Email)

