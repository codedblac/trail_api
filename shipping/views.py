from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

from .models import ShippingAddress, ShippingMethod, Shipment, ShipmentHistory
from .serializers import (
    ShippingAddressSerializer,
    ShippingMethodSerializer,
    ShipmentSerializer,
    ShipmentHistorySerializer,
)


# ----------------------------
# SHIPPING ADDRESS
# ----------------------------
class ShippingAddressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing customer shipping addresses.
    Users can create, update, delete and set default addresses.
    """
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Restrict to addresses owned by the logged-in user
        return ShippingAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Enforce logged-in user (prevents spoofing)
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def set_default(self, request, pk=None):
        """
        Set an address as the default address for the user
        """
        address = self.get_object()
        ShippingAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)
        address.is_default = True
        address.save()
        return Response({"status": "default address set"})


# ----------------------------
# SHIPPING METHODS
# ----------------------------
class ShippingMethodListView(generics.ListAPIView):
    """
    List available shipping methods.
    """
    queryset = ShippingMethod.objects.filter(is_active=True)
    serializer_class = ShippingMethodSerializer
    permission_classes = [permissions.AllowAny]


# ----------------------------
# SHIPMENTS
# ----------------------------
class ShipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing shipments linked to orders.
    - Customers can view their own shipment status.
    - Admin/staff can create and update shipment status.
    """
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Shipment.objects.all()
        return Shipment.objects.filter(order__user=user)

    def perform_create(self, serializer):
        """
        Only admins should create shipments (linked to orders).
        """
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Only admins can create shipments.")
        serializer.save()

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        """
        Admin/staff can update shipment status and record history.
        """
        shipment = self.get_object()
        old_status = shipment.status
        new_status = request.data.get("status")

        if new_status not in dict(Shipment.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        shipment.status = new_status

        # Automatically set timestamps
        if new_status == "shipped" and not shipment.shipped_at:
            shipment.shipped_at = timezone.now()
        elif new_status == "delivered" and not shipment.delivered_at:
            shipment.delivered_at = timezone.now()

        shipment.save()

        # Record history
        ShipmentHistory.objects.create(
            shipment=shipment,
            old_status=old_status,
            new_status=new_status,
            note=request.data.get("note", "")
        )

        return Response({"status": f"Shipment updated to {new_status}"})


# ----------------------------
# SHIPMENT HISTORY
# ----------------------------
class ShipmentHistoryListView(generics.ListAPIView):
    """
    List shipment history for a given shipment.
    """
    serializer_class = ShipmentHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        shipment_id = self.kwargs.get("shipment_id")
        qs = ShipmentHistory.objects.filter(shipment_id=shipment_id)

        # Restrict to owner unless staff
        if not self.request.user.is_staff:
            qs = qs.filter(shipment__order__user=self.request.user)
        return qs
