from rest_framework import serializers
from .models import Payment, PaymentLog


class PaymentLogSerializer(serializers.ModelSerializer):
    """Serializer for raw payment logs (M-Pesa callbacks, etc.)"""

    class Meta:
        model = PaymentLog
        fields = ["id", "payment", "payload", "created_at"]
        read_only_fields = ["id", "created_at"]


class PaymentSerializer(serializers.ModelSerializer):
    """General serializer for viewing payment details"""

    logs = PaymentLogSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "user",
            "method",
            "amount",
            "transaction_id",
            "status",
            "created_at",
            "updated_at",
            # M-Pesa fields
            "phone_number",
            "merchant_request_id",
            "checkout_request_id",
            "result_code",
            "result_description",
            # Bank transfer fields
            "reference_number",
            "receipt_image",
            # Related logs
            "logs",
        ]
        read_only_fields = [
            "id",
            "status",
            "transaction_id",
            "merchant_request_id",
            "checkout_request_id",
            "result_code",
            "result_description",
            "created_at",
            "updated_at",
            "logs",
        ]


class MpesaPaymentInitSerializer(serializers.ModelSerializer):
    """
    Serializer for initiating an M-Pesa STK Push.
    Requires order, amount (validated), and phone number.
    """

    class Meta:
        model = Payment
        fields = ["order", "amount", "phone_number"]

    def validate(self, attrs):
        order = attrs.get("order")
        amount = attrs.get("amount")

        if order.payment:  # One-to-one relation, ensure no duplicate
            raise serializers.ValidationError("This order already has a payment.")

        if amount <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")

        return attrs


class BankTransferSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading proof of a bank transfer.
    """

    class Meta:
        model = Payment
        fields = ["order", "amount", "reference_number", "receipt_image"]

    def validate(self, attrs):
        order = attrs.get("order")
        amount = attrs.get("amount")

        if order.payment:
            raise serializers.ValidationError("This order already has a payment.")

        if amount <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")

        return attrs
