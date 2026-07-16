from django.urls import path,include
from rest_framework.routers import DefaultRouter
from Admin import views

router = DefaultRouter()
router.register ('category',views.CategoryViewSet,basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.AdminDashboard.as_view(), name='admin-dashboard'),
    path('register/',views.RegisterDelivererView.as_view(),name='register-deliverer'),
    path('orders/<int:order_id>/assign/',views.AssignDelivererView.as_view(),name='assign-deliverer'),
]