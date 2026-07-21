<<<<<<< Updated upstream
from Center.models import Deliverer,Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



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
=======
from django.shortcuts import render

# Create your views here.

>>>>>>> Stashed changes
