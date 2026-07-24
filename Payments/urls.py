from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MakePaymentViewsets, pay_order, stk_callback, pay_deliverer, b2c_callback

router = DefaultRouter()
router.register("payments", MakePaymentViewsets, basename="payments")
# router.register("makepayments", MakePaymentViewsets, basename="payments")


urlpatterns = [
    path('', include(router.urls)),
    path('pay-order/', pay_order),
    path('pay-deliverer/', pay_deliverer),
    path('stk/callback', stk_callback, name='stk_callback'),
    path('b2c/callback', b2c_callback),
]