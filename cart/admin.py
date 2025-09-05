from django.contrib import admin
from .models import Cart, CartItem, Coupon


class CartItemInline(admin.TabularInline):
    """
    Inline view of CartItems inside Cart admin.
    """
    model = CartItem
    extra = 0
    readonly_fields = ("product", "price", "subtotal", "added_at")
    fields = ("product", "quantity", "price", "subtotal", "added_at")

    def subtotal(self, obj):
        return obj.subtotal


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Admin for Carts with inline items.
    """
    list_display = ("id", "user", "session_id", "total_items", "total_price", "is_active", "updated_at")
    list_filter = ("is_active", "updated_at", "created_at")
    search_fields = ("user__username", "session_id")
    readonly_fields = ("total_items", "total_price", "created_at", "updated_at")
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Admin for individual Cart Items.
    """
    list_display = ("id", "cart", "product", "quantity", "price", "subtotal", "added_at")
    list_filter = ("added_at",)
    search_fields = ("product__name", "cart__id")

    readonly_fields = ("subtotal",)

    def subtotal(self, obj):
        return obj.subtotal


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """
    Admin for Coupons (discount codes).
    """
    list_display = ("code", "discount_percent", "active", "valid_from", "valid_to", "is_valid_now")
    list_filter = ("active", "valid_from", "valid_to")
    search_fields = ("code",)
    readonly_fields = ("is_valid_now",)

    def is_valid_now(self, obj):
        return obj.is_valid()
    is_valid_now.boolean = True  # ✅ shows green check or red X
