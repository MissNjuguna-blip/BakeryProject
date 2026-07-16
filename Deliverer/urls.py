from django.urls import path
from Deliverer import views

urlpatterns = [
    path('Orders/add/',views.Order),
    path('dashboard/', views.DelivererDashboard.as_view(), name='deliverer-dashboard'),
]
