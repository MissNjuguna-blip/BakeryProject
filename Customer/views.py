from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from Center.models import Customer, Order


class CustomerDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            customer = request.user.customer_profile

            orders = Order.objects.filter(customer=customer)

            data = {
                "customer": customer.user.username,
                "total_orders": orders.count(),
                "pending_orders": orders.filter(status="pending").count(),
                "received_orders": orders.filter(status="received").count(),
                "preparing_orders": orders.filter(status="preparing").count(),
                "ready_orders": orders.filter(status="ready").count(),
                "delivered_orders": orders.filter(status="delivered").count(),
                "cancelled_orders": orders.filter(status="cancelled").count(),
            }

            return Response(data)

        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )