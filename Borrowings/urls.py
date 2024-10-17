from django.urls import path, include
from rest_framework import routers

from Borrowings.views import BorrowingViewSet

borrowing_router = routers.DefaultRouter()
borrowing_router.register(prefix="", viewset=BorrowingViewSet)

urlpatterns = [path("", include(borrowing_router.urls))]

app_name = "borrowings"
