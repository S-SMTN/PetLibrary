from typing import Type

from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Borrowings.factories import BorrowingFactory
from Borrowings.models import Borrowing
from Borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingCreateSerializer
)
from PetLibrary.utils.paginations import ViewPagination


class BorrowingFactoryView(APIView):
    permission_classes = [IsAdminUser,]
    authentication_classes = (JWTAuthentication,)

    def post(self, request: Request, *args, **kwargs) -> Response:
        serialized_borrowings = []
        borrowings = BorrowingFactory.create_batch(10)
        for borrowing in borrowings:
            serializer = BorrowingListSerializer(borrowing)
            serialized_borrowings.append(serializer.data)

        return Response(serialized_borrowings, status=status.HTTP_201_CREATED)


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
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def perform_create(self, serializer: BorrowingSerializer) -> None:
        serializer.save(user=self.request.user)
