from django.db import models
from django.conf import settings
from orders.models import Order

User = settings.AUTH_USER_MODEL


class Payment(models.Model):
    """
    Master payment model — every payment (M-Pesa or Bank Transfer) is recorded here.
    One-to-one linked to an order.
    """

    METHOD_CHOICES = [
        ("mpesa", "M-Pesa"),
        ("bank", "Bank Transfer"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("initiated", "Initiated"),   # STK push sent, awaiting user input
        ("successful", "Successful"),
        ("failed", "Failed"),
        ("reversed", "Reversed"),
    ]

    order = models.OneToOneField(Order, related_name="payment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # M-Pesa specific
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    merchant_request_id = models.CharField(max_length=100, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    result_code = models.CharField(max_length=10, blank=True, null=True)
    result_description = models.TextField(blank=True, null=True)

    # Bank Transfer specific
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    receipt_image = models.ImageField(upload_to="bank_receipts/", blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.method.upper()} | {self.amount} | {self.status}"


class PaymentLog(models.Model):
    """
    Keeps raw logs from M-Pesa callbacks or Bank confirmations
    for debugging and audit trail.
    """

    payment = models.ForeignKey(Payment, related_name="logs", on_delete=models.CASCADE)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for Payment {self.payment.id} at {self.created_at}"
