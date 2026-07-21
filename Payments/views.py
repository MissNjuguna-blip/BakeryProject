from django.shortcuts import render
<<<<<<< Updated upstream
from rest_framework import viewsets,permissions
from rest_framework.permissions import IsAuthenticated
from Center.models import Payment, User
from rest_framework.exceptions import PermissionDenied
from .serializer import PaymentCreateSerializer,PaymentSerializer,AdminPaymentSerializer

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

=======

# Create your views here.
>>>>>>> Stashed changes
