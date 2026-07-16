from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework import viewsets,status
from Admin.serializer import CategorySerializer,AssignDelivererSerializer,DelivererCreateSerializer
from Center.models import Category
from Center.models import Admin, Customer, Deliverer, Product,Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class CategoryViewSet (viewsets.ModelViewSet):
    model = Category
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

# Admin Dasshboard
class AdminDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            admin = request.user.admin_profile

            data = {
                "admin": admin.user.username,
                "customers": Customer.objects.count(),
                "deliverers": Deliverer.objects.count(),
                "products": Product.objects.count(),
                "orders": Order.objects.count(),
                "pending_orders": Order.objects.filter(status="pending").count(),
                "completed_orders": Order.objects.filter(status="delivered").count(),
            }

            return Response(data)

        except Admin.DoesNotExist:
            return Response(
                {"error": "Admin profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
# Create Deliverer

class RegisterDelivererView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != "ADMIN":
            return Response(
                {"error": "Only admins can register deliverers."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = DelivererCreateSerializer(data=request.data)

        if serializer.is_valid():
            deliverer = serializer.save()

            return Response(
                {
                    "message": "Deliverer registered successfully.",
                    "id": deliverer.id,
                    "name": deliverer.name,
                    "username": deliverer.user.username,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Assign Deliverer to Order
class AssignDelivererView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):

        if request.user.role != "ADMIN":
            return Response(
                {"error": "Only admins can assign deliverers."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AssignDelivererSerializer(data=request.data)

        if serializer.is_valid():

            try:
                order = Order.objects.get(id=order_id)

                if order.deliverer:
                    return Response(
                        {"error": "This order already has a deliverer."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                deliverer = Deliverer.objects.get(
                    id=serializer.validated_data["deliverer_id"]
                )

                order.deliverer = deliverer
                order.status = "received"
                order.save()

                deliverer.available = False
                deliverer.save()

                return Response(
                    {
                        "message": "Deliverer assigned successfully.",
                        "order": order.id,
                        "deliverer": deliverer.name,
                    },
                    status=status.HTTP_200_OK,
                )

            except Order.DoesNotExist:
                return Response(
                    {"error": "Order not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            except Deliverer.DoesNotExist:
                return Response(
                    {"error": "Deliverer not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)