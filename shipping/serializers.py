from rest_framework import serializers
from .models import ShippingAddress, ShippingMethod, Shipment, ShipmentHistory


# ----------------------------
# SHIPPING ADDRESS
# ----------------------------
class ShippingAddressSerializer(serializers.ModelSerializer):
    """
    Serializer for customer shipping addresses
    """
    class Meta:
        model = ShippingAddress
        fields = [
            "id",
            "user",
            "full_name",
            "phone_number",
            "email",
            "country",
            "city",
            "postal_code",
            "street_address",
            "landmark",
            "is_default",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "user"]

    def create(self, validated_data):
        # Automatically assign the user from request context
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


# ----------------------------
# SHIPPING METHOD
# ----------------------------
class ShippingMethodSerializer(serializers.ModelSerializer):
    """
    Serializer for available shipping methods
    """
    class Meta:
        model = ShippingMethod
        fields = [
            "id",
            "name",
            "description",
            "base_cost",
            "cost_per_km",
            "estimated_days",
            "is_active",
        ]
        read_only_fields = ["id"]


# ----------------------------
# SHIPMENT HISTORY
# ----------------------------
class ShipmentHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for shipment status history
    """
    class Meta:
        model = ShipmentHistory
        fields = [
            "id",
            "old_status",
            "new_status",
            "changed_at",
            "note",
        ]
        read_only_fields = ["id", "changed_at"]


# ----------------------------
# SHIPMENT
# ----------------------------
class ShipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for order shipment
    Includes nested shipping address, method, and history
    """
    address = ShippingAddressSerializer(read_only=True)
    method = ShippingMethodSerializer(read_only=True)
    history = ShipmentHistorySerializer(many=True, read_only=True)

    # Write-only IDs for linking
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=ShippingAddress.objects.all(),
        source="address",
        write_only=True,
    )
    method_id = serializers.PrimaryKeyRelatedField(
        queryset=ShippingMethod.objects.all(),
        source="method",
        write_only=True,
        required=False,
    )

    class Meta:
        model = Shipment
        fields = [
            "id",
            "order",
            "address",
            "method",
            "courier_name",
            "tracking_number",
            "status",
            "shipped_at",
            "delivered_at",
            "created_at",
            "history",
            "address_id",
            "method_id",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "history",
            "order",  # 🚨 important: users shouldn't assign order manually
        ]
