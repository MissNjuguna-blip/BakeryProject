from django.urls import path,include
from rest_framework.routers import DefaultRouter
from Favorite import views

router = DefaultRouter()
router.register(r"favorites", views.FavoriteViewSet, basename="favorites")
urlpatterns = [
    path ('' ,include(router.urls))
]