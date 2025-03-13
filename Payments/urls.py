from django.urls import path, include
from rest_framework import routers

from Payments.views import (
    PaymentListRetrieveVewSet,
    PaymentSuccessView,
    PaymentCancelView,
)

payment_router = routers.DefaultRouter()
payment_router.register(prefix="list", viewset=PaymentListRetrieveVewSet)

urlpatterns = [
    path("", include(payment_router.urls)),
    path("success/", PaymentSuccessView.as_view(), name="success"),
    path("cancel/", PaymentCancelView.as_view(), name="cancel"),
]

app_name = "payments"
