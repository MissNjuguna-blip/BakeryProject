from django.urls import path, include
from Customer import views

urlpatterns = [
    path('dashboard/', views.CustomerDashboard.as_view(), name='customer-dashboard'),

]