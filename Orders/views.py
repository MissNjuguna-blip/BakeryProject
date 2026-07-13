from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from Center.models import Order
from Orders.serializer import (OrderSerializer,CreateOrderSerializer)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


    def get_serializer_class(self):
    
        if self.action == "create":
            return CreateOrderSerializer

        return OrderSerializer


    def get_queryset(self):

        user = self.request.user

        # Admin/Baker sees every order
        if user.role in ["admin"]:
            return Order.objects.all()

        # Customer sees only their own orders
        elif user.role == "customer":
            return Order.objects.filter(
                customer__user=user
            )

        # Deliverer sees assigned deliveries only
        elif user.role == "deliverer":
            return Order.objects.filter(
                deliverer__user=user
            )
        # Anything else sees nothing
        return Order.objects.none()



    def perform_create(self, serializer):
        user = self.request.user

        if user.role != "customer":
            raise PermissionDenied(
                "Only customers can place orders."
            )

        serializer.save()

    def update(self, request, *args, **kwargs):
       
        user = request.user

        if user.role not in ["admin", "baker", "deliverer"]:
            raise PermissionDenied(
                "You do not have permission to update orders."
            )

        return super().update(request,*args,**kwargs)