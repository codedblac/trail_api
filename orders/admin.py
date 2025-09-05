from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, OrderHistory


# ----------------------------
# ORDER ITEM INLINE
# ----------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "price", "subtotal")
    fields = ("product", "quantity", "price", "subtotal")
    can_delete = False


# ----------------------------
# ORDER HISTORY INLINE
# ----------------------------
class OrderHistoryInline(admin.TabularInline):
    model = OrderHistory
    extra = 0
    readonly_fields = ("status", "changed_at", "note")
    fields = ("status", "changed_at", "note")
    can_delete = False


# ----------------------------
# ORDER ADMIN
# ----------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "status_colored",
        "payment_method",
        "payment_status",
        "total",
        "created_at",
    )
    list_filter = (
        "status",
        "payment_status",
        "payment_method",
        "created_at",
    )
    search_fields = ("id", "email", "full_name", "phone_number")
    readonly_fields = (
        "subtotal",
        "discount",
        "total",
        "created_at",
        "updated_at",
        "payment_id",
    )
    inlines = [OrderItemInline, OrderHistoryInline]
    ordering = ("-created_at",)

    fieldsets = (
        ("Customer Info", {
            "fields": ("user", "full_name", "email", "phone_number")
        }),
        ("Addresses", {
            "fields": ("shipping_address", "billing_address")
        }),
        ("Order Details", {
            "fields": ("status", "payment_method", "payment_status", "payment_id")
        }),
        ("Totals", {
            "fields": ("subtotal", "discount", "total")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def status_colored(self, obj):
        colors = {
            "pending": "orange",
            "paid": "green",
            "shipped": "blue",
            "delivered": "purple",
            "cancelled": "red",
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, "black"),
            obj.status.capitalize()
        )
    status_colored.short_description = "Status"


# ----------------------------
# ORDER ITEM ADMIN
# ----------------------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "subtotal")
    list_filter = ("order__status", "product")
    search_fields = ("order__id", "product__name")
    ordering = ("-order",)


# ----------------------------
# ORDER HISTORY ADMIN
# ----------------------------
@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ("order", "status", "changed_at", "note")
    list_filter = ("status", "changed_at")
    search_fields = ("order__id", "status", "note")
    ordering = ("-changed_at",)
