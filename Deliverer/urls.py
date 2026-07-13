from django.urls import path
from Deliverer import views

urlpatterns = [
    path('Orders/add/',views.Orders)
]
