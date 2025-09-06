from django.contrib import admin
from django.utils import timezone
from .models import ShippingAddress, ShippingMethod, Shipment, ShipmentHistory


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "phone_number",
        "city",
        "country",
        "is_default",
        "created_at",
    )
    list_filter = ("country", "city", "is_default", "created_at")
    search_fields = ("full_name", "phone_number", "email", "city", "street_address")
    ordering = ("-created_at",)
    list_per_page = 25


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "base_cost",
        "cost_per_km",
        "estimated_days",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "estimated_days")
    search_fields = ("name", "description")
    ordering = ("base_cost",)
    list_editable = ("is_active",)  # quick toggle active/inactive
    list_per_page = 25


class ShipmentHistoryInline(admin.TabularInline):
    model = ShipmentHistory
    extra = 0
    readonly_fields = ("old_status", "new_status", "changed_at", "note")
    can_delete = False
    ordering = ("-changed_at",)


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
    search_fields = (
        "order__id",
        "tracking_number",
        "courier_name",
        "address__city",
        "address__full_name",
    )
    ordering = ("-created_at",)
    inlines = [ShipmentHistoryInline]
    list_per_page = 25

    # ------------------
    # Custom Actions
    # ------------------
    actions = ["mark_as_shipped", "mark_as_delivered", "mark_as_cancelled"]

    def mark_as_shipped(self, request, queryset):
        updated = 0
        for shipment in queryset:
            old_status = shipment.status
            shipment.status = "shipped"
            shipment.shipped_at = timezone.now()
            shipment.save()
            ShipmentHistory.objects.create(
                shipment=shipment,
                old_status=old_status,
                new_status="shipped",
                note="Bulk action: Marked as shipped",
            )
            updated += 1
        self.message_user(request, f"{updated} shipments marked as shipped.")

    mark_as_shipped.short_description = "Mark selected shipments as Shipped"

    def mark_as_delivered(self, request, queryset):
        updated = 0
        for shipment in queryset:
            old_status = shipment.status
            shipment.status = "delivered"
            shipment.delivered_at = timezone.now()
            shipment.save()
            ShipmentHistory.objects.create(
                shipment=shipment,
                old_status=old_status,
                new_status="delivered",
                note="Bulk action: Marked as delivered",
            )
            updated += 1
        self.message_user(request, f"{updated} shipments marked as delivered.")

    mark_as_delivered.short_description = "Mark selected shipments as Delivered"

    def mark_as_cancelled(self, request, queryset):
        updated = 0
        for shipment in queryset:
            old_status = shipment.status
            shipment.status = "cancelled"
            shipment.save()
            ShipmentHistory.objects.create(
                shipment=shipment,
                old_status=old_status,
                new_status="cancelled",
                note="Bulk action: Marked as cancelled",
            )
            updated += 1
        self.message_user(request, f"{updated} shipments marked as cancelled.")

    mark_as_cancelled.short_description = "Mark selected shipments as Cancelled"


@admin.register(ShipmentHistory)
class ShipmentHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "shipment", "old_status", "new_status", "changed_at", "note")
    list_filter = ("new_status", "changed_at")
    search_fields = ("shipment__id", "old_status", "new_status", "note")
    ordering = ("-changed_at",)
    list_per_page = 50
