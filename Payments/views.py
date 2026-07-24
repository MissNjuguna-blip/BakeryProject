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
    """Initiate STK push to customer's phone"""
    order_id = request.data.get("order_id")
    phone = request.data.get("phone")

    try:
        order = Order.objects.get(id=order_id, customer__user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    mpesa = MpesaPayment()
    result = mpesa.customer_payment(phone, order.total_amount, order.id)

    return Response(result)


@csrf_exempt
def stk_callback(request):
    """Safaricom sends STK push result here"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid payload"})
    print("========== STK CALLBACK ==========")
    print(json.dumps(data, indent=2))
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})


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

