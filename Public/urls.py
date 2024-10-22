import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from Payments.views import StripeWebhookView
from Public.views import LibraryViewSet

library_router = routers.DefaultRouter()
library_router.register(prefix="", viewset=LibraryViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/library/", include(library_router.urls)),
    path("api/user/", include("Users.urls", namespace="User")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("api/payments/webhook/stripe/", StripeWebhookView.as_view(), name="stripe-webhook")
]
