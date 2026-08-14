from django.urls import path, include
from Customer import views

urlpatterns = [
    path('dashboard/', views.CustomerDashboard.as_view(), name='customer-dashboard'),
    path("favorites/", views.FavoriteList.as_view()),
    path("favorite/<int:product_id>/", views.ToggleFavorite.as_view()),

]
