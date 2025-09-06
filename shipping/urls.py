from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShippingAddressViewSet,
    ShippingMethodListView,
    ShipmentViewSet,
    ShipmentHistoryListView,
)

# Router for address + shipment ViewSets
router = DefaultRouter()
router.register(r"addresses", ShippingAddressViewSet, basename="shipping-address")
router.register(r"shipments", ShipmentViewSet, basename="shipment")

urlpatterns = [
    path("", include(router.urls)),

    # List available shipping methods
    path("methods/", ShippingMethodListView.as_view(), name="shipping-method-list"),

    # Shipment history (tracking timeline)
    path(
        "shipments/<int:shipment_id>/history/",
        ShipmentHistoryListView.as_view(),
        name="shipment-history-list",
    ),
]
