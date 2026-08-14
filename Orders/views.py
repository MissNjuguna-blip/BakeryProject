from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from Center.models import Order
from Orders.serializer import (
    OrderSerializer,
    CreateOrderSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):

        if self.action == "create":
            return CreateOrderSerializer

        return OrderSerializer

    def get_queryset(self):

        user = self.request.user

        # Admin sees all orders
        if user.role == "ADMIN":
            return Order.objects.all()

        # Customer sees only their orders
        elif user.role == "CUSTOMER":
            return Order.objects.filter(
                customer__user=user
            )

        # Deliverer sees assigned orders
        elif user.role == "DELIVERER":
            return Order.objects.filter(
                deliverer__user=user
            )

        return Order.objects.none()

    def perform_create(self, serializer):

        user = self.request.user

        if user.role != "CUSTOMER":
            raise PermissionDenied(
                "Only customers can place orders."
            )

        serializer.save()

    def create(self, request, *args, **kwargs):

        user = request.user

        if user.role != "CUSTOMER":
            raise PermissionDenied(
                "Only customers can place orders."
            )

        # Validate incoming order
        serializer = CreateOrderSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        # Create order
        order = serializer.save()

        # Serialize the CREATED order using the read serializer
        response_serializer = OrderSerializer(
            order,
            context={"request": request}
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):

        user = request.user

        if user.role not in [
            "ADMIN",
            "BAKER",
            "DELIVERER"
        ]:
            raise PermissionDenied(
                "You do not have permission to update orders."
            )

        return super().update(
            request,
            *args,
            **kwargs
        )