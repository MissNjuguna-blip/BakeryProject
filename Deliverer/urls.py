from django.urls import path
from Deliverer import views

urlpatterns = [
<<<<<<< Updated upstream
    path('Orders/add/',views.Order),
    path('dashboard/', views.DelivererDashboard.as_view(), name='deliverer-dashboard'),
=======
    path('Orders/add/',views.Orders)
>>>>>>> Stashed changes
]
