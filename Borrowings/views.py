from typing import Type

from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from Borrowings.factories import BorrowingFactory
from Borrowings.models import Borrowing
from Borrowings.serializers import BorrowingSerializer, BorrowingListSerializer
from PetLibrary.utils.paginations import ViewPagination


def factory_borrowing(request: HttpRequest):
    borrowings = BorrowingFactory.create_batch(10)

    return HttpResponse(f"{[str(borrowing) for borrowing in borrowings]}")


class BorrowingViewSet(ModelViewSet):
    queryset = Borrowing.objects.all().prefetch_related(
        "books",
        "books__author"
    )
    serializer_class = BorrowingSerializer
    pagination_class = ViewPagination

    def get_permissions(self) -> list[IsAdminUser] | list[IsAuthenticated]:
        if self.action in ("create", "list", "retrieve"):
            return [IsAuthenticated(),]
        return [IsAdminUser(),]

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_staff:
            return self.queryset.select_related(
                "user",
            )
        return self.queryset.filter(user__id=self.request.user.id)

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action in ("list", "retrieve"):
            return BorrowingListSerializer
        return BorrowingSerializer
