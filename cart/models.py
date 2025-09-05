from django.db import models
from django.conf import settings
from django.utils import timezone
from products.models import Product  # your existing product model

User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    """
    A shopping cart. Can belong to a user (logged-in) or
    a guest via session_id. Each cart can hold multiple CartItems.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="carts"
    )
    session_id = models.CharField(
        max_length=255, null=True, blank=True, help_text="For guest carts"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        if self.user:
            return f"Cart {self.id} (User: {self.user})"
        return f"Cart {self.id} (Guest)"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    def clear(self):
        """Remove all items from the cart."""
        self.items.all().delete()


class CartItem(models.Model):
    """
    An item inside a cart. Stores a snapshot of product price
    to protect against future price changes.
    """
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Price snapshot at the time of adding"
    )
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("cart", "product")
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    @property
    def subtotal(self):
        return self.price * self.quantity


class Coupon(models.Model):
    """
    Optional: For applying discounts on carts or orders.
    """
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    class Meta:
        ordering = ["-valid_from"]

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to
