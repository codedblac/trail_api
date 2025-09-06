from rest_framework import serializers
from .models import Order, OrderItem, OrderHistory
from cart.models import Cart
from shipping.models import ShippingAddress, ShippingMethod


# ----------------------------
# ORDER ITEM
# ----------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    # Flatten product details for frontend
    name = serializers.CharField(source="product.name", read_only=True)
    image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "name", "price", "quantity", "image"]


# ----------------------------
# ORDER HISTORY
# ----------------------------
class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ["id", "status", "changed_at", "note"]


# ----------------------------
# SHIPPING ADDRESS (nested)
# ----------------------------
class ShippingAddressSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    postalCode = serializers.CharField(source="postal_code")

    class Meta:
        model = ShippingAddress
        fields = ["firstName", "lastName", "address", "city", "postalCode"]


# ----------------------------
# ORDER (READ-ONLY)
# ----------------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    history = OrderHistorySerializer(many=True, read_only=True)
    shippingAddress = ShippingAddressSerializer(source="shipping_address", read_only=True)

    # Map fields to frontend naming conventions
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    estimatedDelivery = serializers.CharField(read_only=True, required=False)
    trackingNumber = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "total",
            "createdAt",
            "updatedAt",
            "estimatedDelivery",
            "trackingNumber",
            "items",
            "shippingAddress",
            "history",
        ]
        read_only_fields = fields


# ----------------------------
# ORDER CREATE (CHECKOUT)
# ----------------------------
class OrderCreateSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(write_only=True)
    shipping_address_id = serializers.IntegerField(write_only=True)
    shipping_method_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "cart_id",
            "email",
            "full_name",
            "phone_number",
            "shipping_address_id",
            "shipping_method_id",
        ]

    def create(self, validated_data):
        cart_id = validated_data.pop("cart_id")
        shipping_address_id = validated_data.pop("shipping_address_id")
        shipping_method_id = validated_data.pop("shipping_method_id")

        user = (
            self.context["request"].user
            if self.context["request"].user.is_authenticated
            else None
        )

        # ✅ Get cart
        try:
            cart = Cart.objects.get(id=cart_id, is_active=True)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive cart.")

        # ✅ Get shipping address
        try:
            shipping_address = ShippingAddress.objects.get(
                id=shipping_address_id, user=user
            )
        except ShippingAddress.DoesNotExist:
            raise serializers.ValidationError("Invalid shipping address.")

        # ✅ Get shipping method
        try:
            shipping_method = ShippingMethod.objects.get(
                id=shipping_method_id, is_active=True
            )
        except ShippingMethod.DoesNotExist:
            raise serializers.ValidationError("Invalid shipping method.")

        # ✅ Create order
        order = Order.objects.create(
            user=user,
            shipping_address=shipping_address,
            shipping_method=shipping_method,
            **validated_data,
        )

        # ✅ Calculate totals
        subtotal = 0
        for item in cart.items.all():
            subtotal += item.subtotal
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price,
                subtotal=item.subtotal,
            )

        discount = cart.coupon.discount_amount if hasattr(cart, "coupon") and cart.coupon else 0
        shipping_cost = shipping_method.base_cost
        total = subtotal - discount + shipping_cost

        order.subtotal = subtotal
        order.discount = discount
        order.shipping_cost = shipping_cost
        order.total = total
        order.save()

        # ✅ Clear cart
        cart.is_active = False
        cart.save()

        return order
