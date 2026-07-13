from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import MakePaymentViewsets

router = DefaultRouter()
router.register("payments", MakePaymentViewsets, basename="payments")
# router.register("makepayments", MakePaymentViewsets, basename="payments")


urlpatterns = [
    path ('',include(router.urls))
]