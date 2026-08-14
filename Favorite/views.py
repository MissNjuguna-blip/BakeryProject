from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from Center.models import Favorite
from Favorite.serializer import FavoriteSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(customer=self.request.user.customer_profile)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer_profile)