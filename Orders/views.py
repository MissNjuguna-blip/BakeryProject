<<<<<<< Updated upstream
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
=======
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from Center.models import Customer, Deliverer, Order
from rest_framework.response import Response


# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Orders(request):
    # get the logged in user
    try:
        deliverer = request.user.Deliverer
    except Deliverer.DoesNotExist:
        return Response({'error':'No deliverer account'})

    try:
        phone = request.data.get("phone")
        customer = Customer.objects.get(phone=phone)
    except Customer.DoesNotExist:
        return Response({'error':'No custmer account'})
    
    orders = Order.objects.create(
        customer=customer,
        deliverer=deliverer,
        product=request.data.get("products"),
        total_amount=request.data.get("total_amount")
    )

    return Response ({
        'message':'Orders recorded successfully',
        "orders_id":orders.id,
        "customer":f'{customer.username} {customer.phone}',
        "deliverer":f'{deliverer.name} {deliverer.available}',
        # "Orders":orders.product,
    })
>>>>>>> Stashed changes
