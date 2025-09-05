from rest_framework import serializers
from .models import Cart, CartItem, Coupon
from products.serializers import ProductSerializer  # assuming you already have this


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for a single Cart Item.
    Includes product details and subtotal.
    """
    product = ProductSerializer(read_only=True)  # nested product details
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "price",
            "subtotal",
            "added_at",
        ]


class CartItemCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for adding/updating Cart Items.
    Used when client only sends product_id + quantity.
    """
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

    def create(self, validated_data):
        """
        Handles creation or update of a CartItem.
        Ensures price snapshot is stored.
        """
        cart = self.context["cart"]
        product_id = validated_data.pop("product_id")
        quantity = validated_data.get("quantity", 1)

        from products.models import Product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Invalid product."})

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity, "price": product.price},
        )
        if not created:
            item.quantity += quantity
            item.save()
        return item

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    """
    Full cart serializer with nested items, totals, and coupon support.
    """
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "session_id",
            "is_active",
            "items",
            "total_items",
            "total_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "session_id", "created_at", "updated_at"]


class CouponSerializer(serializers.ModelSerializer):
    """
    Coupon serializer for applying and validating discounts.
    """
    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = ["id", "code", "discount_percent", "active", "valid_from", "valid_to", "is_valid"]

    def get_is_valid(self, obj):
        return obj.is_valid()
