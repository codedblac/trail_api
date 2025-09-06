from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category,
    Brand,
    Product,
    ProductImage,
    HeroBanner,
    ProductVariation,
    ProductReview,
)


# ----------------------------
# CATEGORY ADMIN
# ----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


# ----------------------------
# BRAND ADMIN
# ----------------------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


# ----------------------------
# PRODUCT IMAGE INLINE
# ----------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt_text", "is_featured", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 80px;"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"


# ----------------------------
# PRODUCT VARIATION INLINE
# ----------------------------
class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1
    fields = ("name", "sku", "price", "stock_quantity", "is_active")


# ----------------------------
# PRODUCT ADMIN
# ----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "brand",
        "price",
        "discount_price",
        "stock_quantity",
        "availability",
        "average_rating",
        "is_active",
        "is_featured",
        "is_on_sale",
        "created_at",
    )
    list_filter = (
        "is_active",
        "is_featured",
        "is_on_sale",
        "availability",
        "category",
        "brand",
        "created_at",
    )
    search_fields = ("name", "description", "sku")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    inlines = [ProductImageInline, ProductVariationInline]


# ----------------------------
# PRODUCT IMAGE ADMIN
# ----------------------------
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "is_featured", "alt_text", "created_at", "image_preview")
    list_filter = ("is_featured", "created_at")
    search_fields = ("product__name", "alt_text")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 80px;"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"


# ----------------------------
# HERO BANNER ADMIN
# ----------------------------
@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "is_active", "display_order", "image_preview", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "subtitle")
    readonly_fields = ("image_preview", "created_at", "updated_at")
    ordering = ("display_order",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 80px;"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"


# ----------------------------
# PRODUCT VARIATION ADMIN
# ----------------------------
@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ("product", "name", "sku", "price", "stock_quantity", "is_active")
    list_filter = ("is_active", "product")
    search_fields = ("name", "sku", "product__name")
    ordering = ("product", "name")


# ----------------------------
# PRODUCT REVIEW ADMIN
# ----------------------------
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__name", "user__email", "comment")
    ordering = ("-created_at",)
