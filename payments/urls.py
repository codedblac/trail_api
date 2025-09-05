from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentViewSet,
    MpesaPaymentInitView,
    MpesaCallbackView,
    BankTransferView,
)

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename="payments")

urlpatterns = [
    path("", include(router.urls)),

    # M-Pesa endpoints
    path("mpesa/initiate/", MpesaPaymentInitView.as_view(), name="mpesa-initiate"),
    path("mpesa/callback/", MpesaCallbackView.as_view(), name="mpesa-callback"),

    # Bank transfer endpoint
    path("bank/submit/", BankTransferView.as_view(), name="bank-transfer"),
]
