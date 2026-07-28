<<<<<<< Updated upstream
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from Center.models import Product
from Products.serializer import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(
                "Only the baker can update products."
            )

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(
                "Only the baker can update products."
            )

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(
                "Only the baker can delete products."
            )

        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied(
                "Only the baker can add products."
            )

        serializer.save()
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> Stashed changes
