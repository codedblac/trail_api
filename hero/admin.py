from django.contrib import admin
from .models import HeroSlide


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "badge", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle", "description", "badge")
    ordering = ("order",)

    fieldsets = (
        ("Content", {
            "fields": ("title", "subtitle", "description", "badge", "cta_text", "cta_link")
        }),
        ("Design", {
            "fields": ("background_color", "image")
        }),
        ("Settings", {
            "fields": ("order", "is_active")
        }),
    )
