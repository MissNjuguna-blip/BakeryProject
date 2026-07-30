from django.urls import path
from Deliverer import views

urlpatterns = [
    path('Orders/add/',views.AddOrder.as_view()),
    path('dashboard/', views.DelivererDashboard.as_view(), name='deliverer-dashboard'),
    path('view-orders',views.DelivererOrders.as_view())

]
