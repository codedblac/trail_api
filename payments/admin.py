from django.contrib import admin
from .models import Payment, PaymentLog


class PaymentLogInline(admin.TabularInline):
    model = PaymentLog
    extra = 0
    readonly_fields = ("payload", "created_at")
    can_delete = False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "user",
        "method",
        "amount",
        "status",
        "transaction_id",
        "created_at",
    )
    list_filter = ("method", "status", "created_at")
    search_fields = (
        "transaction_id",
        "reference_number",
        "phone_number",
        "user__email",
        "order__id",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "merchant_request_id",
        "checkout_request_id",
        "result_code",
        "result_description",
    )
    inlines = [PaymentLogInline]

    fieldsets = (
        ("General Info", {
            "fields": (
                "order",
                "user",
                "method",
                "amount",
                "status",
                "transaction_id",
            )
        }),
        ("M-Pesa Details", {
            "fields": (
                "phone_number",
                "merchant_request_id",
                "checkout_request_id",
                "result_code",
                "result_description",
            ),
            "classes": ("collapse",),
        }),
        ("Bank Transfer Details", {
            "fields": ("reference_number", "receipt_image"),
            "classes": ("collapse",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    actions = ["mark_successful", "mark_failed"]

    def mark_successful(self, request, queryset):
        updated = queryset.update(status="successful")
        self.message_user(request, f"{updated} payment(s) marked as successful.")
    mark_successful.short_description = "Mark selected payments as successful"

    def mark_failed(self, request, queryset):
        updated = queryset.update(status="failed")
        self.message_user(request, f"{updated} payment(s) marked as failed.")
    mark_failed.short_description = "Mark selected payments as failed"


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ("id", "payment", "created_at")
    search_fields = ("payment__transaction_id",)
    readonly_fields = ("payment", "payload", "created_at")
    list_filter = ("created_at",)
