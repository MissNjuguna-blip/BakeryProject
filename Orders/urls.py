from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Orders import views

router = DefaultRouter()
router.register('orders', views.OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls))
]