from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem, Coupon
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    CartItemCreateUpdateSerializer,
    CouponSerializer,
)


class CartViewSet(viewsets.ViewSet):
    """
    Cart endpoints:
    - GET /api/cart/ -> retrieve current cart (user or guest)
    - POST /api/cart/items/ -> add item
    - PATCH /api/cart/items/<id>/ -> update quantity
    - DELETE /api/cart/items/<id>/ -> remove item
    - POST /api/cart/clear/ -> empty the cart
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def _get_or_create_cart(self, request):
        """Get existing cart or create one for user or guest."""
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_id=session_id, is_active=True)
        return cart

    def list(self, request):
        """Return the current cart."""
        cart = self._get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="items")
    def add_item(self, request):
        """Add item to cart (or increase quantity)."""
        cart = self._get_or_create_cart(request)
        serializer = CartItemCreateUpdateSerializer(
            data=request.data, context={"cart": cart}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["patch"], url_path="items/(?P<pk>[^/.]+)")
    def update_item(self, request, pk=None):
        """Update quantity of an item in the cart."""
        cart = self._get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=pk, cart=cart)
        serializer = CartItemCreateUpdateSerializer(
            item, data=request.data, partial=True, context={"cart": cart}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["delete"], url_path="items/(?P<pk>[^/.]+)")
    def remove_item(self, request, pk=None):
        """Remove item from the cart."""
        cart = self._get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=pk, cart=cart)
        item.delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def clear(self, request):
        """Empty the cart."""
        cart = self._get_or_create_cart(request)
        cart.clear()
        return Response({"message": "Cart cleared."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def apply_coupon(self, request):
        """Apply a coupon code to the cart."""
        code = request.data.get("code")
        cart = self._get_or_create_cart(request)

        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            return Response({"error": "Invalid coupon code"}, status=status.HTTP_400_BAD_REQUEST)

        if not coupon.is_valid():
            return Response({"error": "Coupon is expired or inactive"}, status=status.HTTP_400_BAD_REQUEST)

        discount = (cart.total_price * coupon.discount_percent) / 100
        discounted_total = cart.total_price - discount

        return Response({
            "cart": CartSerializer(cart).data,
            "coupon": CouponSerializer(coupon).data,
            "discount": discount,
            "final_total": discounted_total,
        })
