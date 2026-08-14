from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from Center.models import Customer, Order,Favorite,Product


class CustomerDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            customer = request.user.customer_profile

            orders = Order.objects.filter(customer=customer)

            featured_products = Product.objects.filter(
                available=True
            ).order_by("-created_at")[:3]

            recent_orders = orders.order_by("-created_at")[:3]

            data = {
                "customer": customer.user.username,
                "phone":customer.phone,
                "address":customer.address,
                "total_orders": orders.count(),
                "pending_orders": orders.filter(status="pending").count(),
                "received_orders": orders.filter(status="received").count(),
                "preparing_orders": orders.filter(status="preparing").count(),
                "ready_orders": orders.filter(status="ready").count(),
                "delivered_orders": orders.filter(status="delivered").count(),
                "cancelled_orders": orders.filter(status="cancelled").count(),
                "favorite_products": customer.favorites.count(),
                "featured_products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "image": product.image.url,
                }
                for product in featured_products
            ],
            "recent_orders": [
                {
                    "id": order.id,
                    "status": order.status,
                    "total_amount": order.total_amount,
                    "created_at": order.created_at,
                }
                for order in recent_orders
            ],

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

# Toggle favourite items
class ToggleFavorite(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        customer = request.user.customer_profile

        favorite, created = Favorite.objects.get_or_create(
            customer=customer,
            product_id=product_id
        )

        if not created:
            favorite.delete()
            return Response({
                "favorite": False,
                "message": "Removed from favorites"
            })

        return Response({
            "favorite": True,
            "message": "Added to favorites"
        })

# Favourite items list
class FavoriteList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = request.user.customer_profile

        favorites = Favorite.objects.filter(customer=customer)

        data = [
            {
                "id": fav.product.id,
                "name": fav.product.name,
                "price": fav.product.price,
                "image": fav.product.image.url,
                "category": fav.product.category.name,
            }
            for fav in favorites
        ]

        return Response(data)