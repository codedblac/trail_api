from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin panel configuration for CustomUser"""

    # Fields shown in the list view
    list_display = ("email", "full_name", "is_staff", "is_active", "role", "date_joined")
    list_filter = ("is_staff", "is_active", "role")
    search_fields = ("email", "full_name")
    ordering = ("-date_joined",)

    # Fieldsets for viewing/editing users
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("full_name", "phone", "address", "city", "postal_code")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "role", "groups", "user_permissions")}),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Fields when creating a user in admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "password1", "password2", "role", "is_active", "is_staff"),
            },
        ),
    )
