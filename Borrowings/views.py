from typing import Type

from django.db.models import QuerySet
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

from Borrowings.factories import BorrowingFactory
from Borrowings.models import Borrowing
from Borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingCreateSerializer, BorrowingUpdateSerializer
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


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Borrowing.objects.all().prefetch_related(
        "books",
        "books__author"
    )
    serializer_class = BorrowingSerializer
    pagination_class = ViewPagination

    @action(
        methods=["POST"],
        detail=True,
        url_path="return_borrowing",
        permission_classes=[IsAuthenticated],
    )
    def return_borrowing(self, request, pk=None) -> Response:
        borrowing = self.get_object()
        serializer = self.get_serializer(borrowing, data={}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        if self.action == "return_borrowing":
            return BorrowingUpdateSerializer
        return BorrowingSerializer

    def perform_create(self, serializer: BorrowingSerializer) -> None:
        serializer.save(user=self.request.user)
