import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets,permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from Center.models import Payment, User, Order, Deliverer
from .serializer import PaymentCreateSerializer,PaymentSerializer,AdminPaymentSerializer
from .services import MpesaPayment

# Create your views here.
class MakePaymentViewsets(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user

        # Admin/Baker can see all payments
        if user.admin:
            return Payment.objects.select_related("user", "order")

        # Customers see only their own payments
        return Payment.objects.filter(user=user).select_related("order")

    def get_serializer_class(self):
        if self.action == "create":
            return PaymentCreateSerializer
        
        if User.admin and self.action in ["update", "partial_update"]:
            return AdminPaymentSerializer

        return PaymentSerializer

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only the baker can update payments.")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only the baker can update payments.")
        return super().partial_update(request, *args, **kwargs)


# ====== M-PESA ENDPOINTS ======

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def pay_order(request):
    order_id_frnt = request.data.get("order_id")
    phone = request.data.get("phone")

    try:
        order = Order.objects.get(id=order_id_frnt, customer__user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    mpesa = MpesaPayment()
    result = mpesa.customer_payment(phone, order.total_amount, order.id)

    checkout_request_id = result.get("CheckoutRequestID")
    merchant_request_id = result.get("MerchantRequestID")
    from django.db import transaction

    if checkout_request_id:
        with transaction.atomic():
            Payment.objects.filter(order=order, status="processing").update(status="cancelled")

            Payment.objects.create(
                user=request.user,
                order=order,
                method="mpesa",
                amount=order.total_amount,
                checkout_request_id=checkout_request_id,
                merchant_request_id=merchant_request_id,
                status="processing",
            )
        return Response(result, status=200)
    # STK push failed to even initiate — nothing to track, just report the error
    return Response(result, status=502)


from django.utils import timezone

@csrf_exempt
def stk_callback(request):
    try:
        data = json.loads(request.body)
        print(data)
    except json.JSONDecodeError:
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid payload"})

    print("========== STK CALLBACK ==========")
    print(json.dumps(data, indent=2))

    try:
        stk_callback = data["Body"]["stkCallback"]
        checkout_request_id = stk_callback["CheckoutRequestID"]
        result_code = stk_callback["ResultCode"]
        result_desc = stk_callback.get("ResultDesc", "")
    except KeyError:
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Malformed payload"})

    try:
        payment = Payment.objects.get(checkout_request_id=checkout_request_id)
    except Payment.DoesNotExist:
        # Acknowledge anyway so Safaricom doesn't keep retrying
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Payment not found, acknowledged"})

    payment.result_desc = result_desc

    if result_code == 0:
        items = stk_callback["CallbackMetadata"]["Item"]
        meta = {item["Name"]: item.get("Value") for item in items}

        payment.status = "paid"
        payment.transaction_id = meta.get("MpesaReceiptNumber")
        payment.paid_at = timezone.now()
        payment.save()

        # Keep the order status in sync
        order = payment.order
        order.status = "received"
        order.save(update_fields=["status"])
    else:
        payment.status = "failed"
        payment.save()
        print(f"Payment failed for order {payment.order.id}: {result_desc}")

    # Always return 0/200, or Safaricom will keep retrying the callback
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})


# happens async in the background, your frontend needs something to poll after showing "check your phone":
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def payment_status(request, order_id):
    try:
        payment = Payment.objects.filter(
            order_id=order_id, order__customer__user=request.user
        ).latest("created_at")
    except Payment.DoesNotExist:
        return Response({"status": "not_found"}, status=404)

    return Response({
        "status": payment.status,
        "transaction_id": payment.transaction_id,
        "result_desc": payment.result_desc,
    })



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def pay_deliverer(request):
    """Send B2C payment to a deliverer"""
    deliverer_id = request.data.get("deliverer_id")
    amount = request.data.get("amount")

    try:
        deliverer = Deliverer.objects.get(id=deliverer_id)
    except Deliverer.DoesNotExist:
        return Response({"error": "Deliverer not found"}, status=404)

    mpesa = MpesaPayment()
    result = mpesa.pay_deliverer(deliverer.phone, amount)

    return Response(result)


@csrf_exempt
def b2c_callback(request):
    """Safaricom sends B2C result here"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid payload"})
    print("========== B2C CALLBACK ==========")
    print(json.dumps(data, indent=2))
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})

