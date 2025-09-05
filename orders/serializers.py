from rest_framework import serializers
from .models import Order, OrderItem, OrderHistory
from products.serializers import ProductSerializer  # Reuse product serializer (read-only)
from cart.models import Cart, CartItem


# ----------------------------
# ORDER ITEM
# ----------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price", "subtotal"]


# ----------------------------
# ORDER HISTORY
# ----------------------------
class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ["id", "status", "changed_at", "note"]


# ----------------------------
# ORDER (READ-ONLY)
# ----------------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    history = OrderHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "email",
            "full_name",
            "phone_number",
            "shipping_address",
            "billing_address",
            "status",
            "payment_method",
            "payment_id",
            "payment_status",
            "subtotal",
            "discount",
            "total",
            "created_at",
            "updated_at",
            "items",
            "history",
        ]
        read_only_fields = (
            "id",
            "user",
            "status",
            "payment_status",
            "subtotal",
            "discount",
            "total",
            "created_at",
            "updated_at",
        )


# ----------------------------
# ORDER CREATE (CHECKOUT)
# ----------------------------
class OrderCreateSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "cart_id",
            "email",
            "full_name",
            "phone_number",
            "shipping_address",
            "billing_address",
            "payment_method",
        ]

    def create(self, validated_data):
        cart_id = validated_data.pop("cart_id")
        user = self.context["request"].user if self.context["request"].user.is_authenticated else None

        # Get cart
        try:
            cart = Cart.objects.get(id=cart_id, is_active=True)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive cart.")

        # Create order
        order = Order.objects.create(user=user, **validated_data)

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

        # Handle coupon
        discount = cart.coupon.discount_amount if cart.coupon else 0
        total = subtotal - discount

        order.subtotal = subtotal
        order.discount = discount
        order.total = total
        order.save()

        # Clear cart
        cart.is_active = False
        cart.save()

        return order
