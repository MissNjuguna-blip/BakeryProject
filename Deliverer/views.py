from Center.models import Deliverer,Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from Deliverer.serializer import OrderSerializer



class DelivererDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            deliverer = request.user.deliverer_profile

            assigned_orders = Order.objects.filter(deliverer=deliverer)

            data = {
                "deliverer": deliverer.name,
                "available": deliverer.available,
                "assigned_orders": assigned_orders.count(),
                "pending_deliveries": assigned_orders.exclude(status="delivered").count(),
                "completed_deliveries": assigned_orders.filter(status="delivered").count(),
            }

            return Response(data)

        except Deliverer.DoesNotExist:
            return Response(
                {"error": "Deliverer profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DelivererOrders(APIView):
        permission_classes = [IsAuthenticated]

def get(self, request):
        try:
            deliverer = request.user.deliverer_profile

            orders = Order.objects.filter(deliverer=deliverer)
            serializer = OrderSerializer(orders, many=True)

            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class AddOrder(APIView):
        permission_classes = [IsAuthenticated]

def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Order created successfully.",
                    "order": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
