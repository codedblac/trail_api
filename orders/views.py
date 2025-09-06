from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Order, OrderHistory
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderHistorySerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    """
    Handles checkout and order management.
    - Users can list and view their orders.
    - Checkout converts cart -> order.
    - Admins can update order status.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        if user.is_authenticated:
            return Order.objects.filter(user=user).select_related(
                "shipping_address", "shipping_method"
            ).prefetch_related("items", "history")
        return Order.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        """Create order during checkout"""
        order = serializer.save()
        # ✅ Log initial history
        OrderHistory.objects.create(
            order=order, 
            status=order.status, 
            note="Order created during checkout"
        )

    # ----------------------------
    # Custom actions
    # ----------------------------
    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        """Admins can update the order status"""
        order = self.get_object()
        new_status = request.data.get("status")
        valid_statuses = dict(Order.STATUS_CHOICES).keys()

        if new_status not in valid_statuses:
            return Response(
                {"error": "Invalid status"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        # Save history
        OrderHistory.objects.create(
            order=order, 
            status=new_status, 
            note="Status updated by admin"
        )

        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def history(self, request, pk=None):
        """Get order history (status changes)"""
        order = self.get_object()
        history = order.history.all()
        return Response(OrderHistorySerializer(history, many=True).data)
