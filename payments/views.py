from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django_daraja.mpesa.core import MpesaClient

from .models import Payment, PaymentLog
from .serializers import (
    PaymentSerializer,
    MpesaPaymentInitSerializer,
    BankTransferSerializer,
    PaymentLogSerializer,
)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View payments (for users/admin).
    """
    queryset = Payment.objects.all().select_related("order", "user")
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Normal users see only their own payments
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        return self.queryset


class MpesaPaymentInitView(APIView):
    """
    Initiate M-Pesa STK Push payment.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MpesaPaymentInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = serializer.validated_data["order"]
        amount = serializer.validated_data["amount"]
        phone_number = serializer.validated_data["phone_number"]

        # Create payment record
        payment = Payment.objects.create(
            order=order,
            user=request.user,
            method="mpesa",
            amount=amount,
            phone_number=phone_number,
            status="initiated",
        )

        # Initiate STK Push via django-daraja
        cl = MpesaClient()
        callback_url = request.build_absolute_uri("/api/payments/mpesa/callback/")
        response = cl.stk_push(
            phone_number,
            amount,
            "174379",  # shortcode (from settings)
            callback_url,
            "Payment for order {}".format(order.id),
        )

        # Save identifiers from Safaricom response
        payment.merchant_request_id = response.get("MerchantRequestID")
        payment.checkout_request_id = response.get("CheckoutRequestID")
        payment.save()

        return Response(
            {"message": "STK Push initiated", "payment": PaymentSerializer(payment).data},
            status=status.HTTP_201_CREATED,
        )


class MpesaCallbackView(APIView):
    """
    Safaricom callback for STK Push.
    """

    permission_classes = [AllowAny]  # Safaricom must be able to POST here

    def post(self, request):
        data = request.data

        # Save raw log
        checkout_request_id = data.get("Body", {}).get("stkCallback", {}).get("CheckoutRequestID")
        payment = Payment.objects.filter(checkout_request_id=checkout_request_id).first()

        if payment:
            PaymentLog.objects.create(payment=payment, payload=data)

            callback = data["Body"]["stkCallback"]
            result_code = callback["ResultCode"]
            result_desc = callback["ResultDesc"]

            payment.result_code = result_code
            payment.result_description = result_desc

            if result_code == 0:  # success
                mpesa_receipt = callback["CallbackMetadata"]["Item"][1]["Value"]
                payment.transaction_id = mpesa_receipt
                payment.status = "successful"
            else:
                payment.status = "failed"

            payment.save()

        return Response({"ResultCode": 0, "ResultDesc": "Accepted"})


class BankTransferView(APIView):
    """
    Upload proof of payment for bank transfer.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BankTransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = serializer.validated_data["order"]
        amount = serializer.validated_data["amount"]
        reference = serializer.validated_data["reference_number"]
        receipt = serializer.validated_data["receipt_image"]

        payment = Payment.objects.create(
            order=order,
            user=request.user,
            method="bank",
            amount=amount,
            reference_number=reference,
            receipt_image=receipt,
            status="pending",  # to be reviewed by admin
        )

        return Response(
            {"message": "Bank transfer submitted", "payment": PaymentSerializer(payment).data},
            status=status.HTTP_201_CREATED,
        )
