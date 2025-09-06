from django.db import models
from django.conf import settings
from orders.models import Order

User = settings.AUTH_USER_MODEL


class ShippingAddress(models.Model):
    """
    Stores customer delivery addresses.
    A user can have multiple addresses, with one default.
    """
    user = models.ForeignKey(User, related_name="shipping_addresses", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    country = models.CharField(max_length=100, default="Kenya")
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    street_address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)  # optional extra info

    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # Ensure only one default address per user
        if self.is_default:
            ShippingAddress.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name}, {self.city}"


class ShippingMethod(models.Model):
    """
    Defines available shipping options (pickup, standard, express).
    """
    name = models.CharField(max_length=100, unique=True)  # e.g., Pickup, Standard Delivery
    description = models.TextField(blank=True)
    base_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cost_per_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # optional dynamic pricing
    estimated_days = models.PositiveIntegerField(default=3)  # delivery time estimate
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["base_cost"]

    def __str__(self):
        return f"{self.name} ({self.base_cost} KES)"


class Shipment(models.Model):
    """
    Tracks delivery of an order.
    """
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("in_transit", "In Transit"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    order = models.OneToOneField(Order, related_name="shipment", on_delete=models.CASCADE)
    address = models.ForeignKey(ShippingAddress, on_delete=models.PROTECT)
    method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, null=True, blank=True)
    courier_name = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Shipment for Order {self.order.id} - {self.status}"


class ShipmentHistory(models.Model):
    """
    Keeps a log of all shipment status updates (audit trail).
    """
    shipment = models.ForeignKey(Shipment, related_name="history", on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20, blank=True, null=True)
    new_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"Shipment {self.shipment.id} changed to {self.new_status} at {self.changed_at}"
