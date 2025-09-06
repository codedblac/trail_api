from django.contrib import admin
from .models import ShippingAddress, ShippingMethod, Shipment, ShipmentHistory


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "phone_number", "city", "is_default", "created_at")
    list_filter = ("city", "country", "is_default")
    search_fields = ("full_name", "phone_number", "email", "city", "street_address")
    ordering = ("-created_at",)


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "base_cost", "cost_per_km", "estimated_days", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    ordering = ("base_cost",)


class ShipmentHistoryInline(admin.TabularInline):
    model = ShipmentHistory
    extra = 0
    readonly_fields = ("old_status", "new_status", "changed_at", "note")
    can_delete = False


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "address",
        "method",
        "courier_name",
        "tracking_number",
        "status",
        "created_at",
    )
    list_filter = ("status", "method", "created_at")
    search_fields = ("order__id", "tracking_number", "courier_name", "address__city")
    ordering = ("-created_at",)
    inlines = [ShipmentHistoryInline]


@admin.register(ShipmentHistory)
class ShipmentHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "shipment", "old_status", "new_status", "changed_at", "note")
    list_filter = ("new_status", "changed_at")
    search_fields = ("shipment__id", "old_status", "new_status", "note")
    ordering = ("-changed_at",)
