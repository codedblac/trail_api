from django.db import models
from django.conf import settings
from django.utils import timezone
from cart.models import Cart, CartItem
from products.models import Product

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_METHODS = [
        ("stripe", "Stripe"),
        ("paypal", "PayPal"),
        ("cod", "Cash on Delivery"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50, blank=True)
    shipping_address = models.TextField()
    billing_address = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="stripe")
    payment_id = models.CharField(max_length=255, blank=True, null=True)  # e.g. Stripe ID
    payment_status = models.CharField(max_length=50, default="unpaid")

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.id} - {self.full_name} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot price
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} × {self.product}"


class OrderHistory(models.Model):
    """Optional: track order status changes for audit/logging"""
    order = models.ForeignKey(Order, related_name="history", on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Order {self.order.id} → {self.status} at {self.changed_at}"
