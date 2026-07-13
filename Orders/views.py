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