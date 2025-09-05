# products/admin.py
from django.contrib import admin
from .models import Product, Category, HeroBanner

# --------------------
# Category Admin
# --------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")

# --------------------
# Product Admin
# --------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "stock", "is_active", "created_at")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("name",)}

    # Optional: show related categories inline
    autocomplete_fields = ["category"]

# --------------------
# Hero Banner Admin
# --------------------
@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active", "display_order", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle")
    ordering = ("display_order",)
    readonly_fields = ("created_at", "updated_at")

