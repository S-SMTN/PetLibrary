from typing import Type

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet

from Books.factories import BookFactory
from Books.models import Author, Book, Tag
from Books.serialaizers import (
    BookSerializer,
    TagSerializer,
    AuthorListSerializer,
    AuthorCreateUpdateSerializer,
    BookListSerializer,
    BookCreateUpdateSerializer
)
from PetLibrary.utils.paginations import ViewPagination
from PetLibrary.utils.permissions import IsAdminOrIfAuthenticatedReadOnly


class BookFactoryView(APIView):
    permission_classes = [IsAdminUser,]
    authentication_classes = (JWTAuthentication,)

    def post(self, request: Request, *args, **kwargs) -> Response:
        serialized_books = []
        for _ in range(10):
            book = BookFactory()
            serializer = BookSerializer(data=book.__dict__)
            serializer.is_valid()
            serialized_books.append(serializer.data)

        return Response(serialized_books, status=status.HTTP_201_CREATED)


class AdminOrAuthenticatedReadOnlyViewSet(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = ViewPagination


class AuthorViewSet(AdminOrAuthenticatedReadOnlyViewSet):
    queryset = Author.objects.all().prefetch_related("tags")
    serializer_class = AuthorListSerializer

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action in ("list", "retrieve"):
            return AuthorListSerializer
        if self.action in ("create", "update"):
            return AuthorCreateUpdateSerializer
        return AuthorListSerializer


class BookViewSet(AdminOrAuthenticatedReadOnlyViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self) -> QuerySet:
        if self.action in ("list", "retrieve", "update"):
            return (
                self.queryset.filter(inventory__gt=0)
                .select_related("author").prefetch_related("tags")
            )

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action in ("list", "retrieve"):
            return BookListSerializer
        if self.action in ("create", "update"):
            return BookCreateUpdateSerializer
        return BookListSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser,]
    pagination_class = ViewPagination
