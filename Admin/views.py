from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework import viewsets
from Admin.serializer import CategorySerializer
from Center.models import Category

# Create your views here.
class CategoryViewSet (viewsets.ModelViewSet):
    model = Category
    serializer_class = CategorySerializer
    queryset = Category.objects.all()