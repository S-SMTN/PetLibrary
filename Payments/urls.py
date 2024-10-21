from django.urls import path, include
from rest_framework import routers

from Payments.views import PaymentListRetrieveVewSet

payment_router = routers.DefaultRouter()
payment_router.register(prefix="list", viewset=PaymentListRetrieveVewSet)

urlpatterns = [
    path("", include(payment_router.urls))
#     path("success/", ), #TODO - check successful stripe payment
#     path("cancel/", ), #TODO - return payment paused message
]

app_name = "payments"
