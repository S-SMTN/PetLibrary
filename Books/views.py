from typing import Type

from django.db.models import QuerySet, Q
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

    @staticmethod
    def _split_str_params(qs: str) -> list[str]:
        return [item.strip() for item in qs.split(",")]

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset

        tags = self.request.query_params.get("tags")
        name = self.request.query_params.get("name")

        if tags:
            tag_names = self._split_str_params(tags)
            queryset = queryset.filter(tags__name__in=tag_names)

        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) | Q(last_name__icontains=name)
            )

        return queryset

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action in ("list", "retrieve"):
            return AuthorListSerializer
        if self.action in ("create", "update"):
            return AuthorCreateUpdateSerializer
        return AuthorListSerializer


class BookViewSet(AdminOrAuthenticatedReadOnlyViewSet):
    queryset = Book.objects.select_related("author").prefetch_related("tags")
    serializer_class = BookSerializer

    @staticmethod
    def _params_to_ints(qs: str) -> list[int]:
        return [int(str_id) for str_id in qs.split(",") if str_id.isdigit()]

    @staticmethod
    def _split_str_params(qs: str) -> list[str]:
        return [item.strip() for item in qs.split(",")]

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if self.action == "list":
            authors = self.request.query_params.get("authors")
            tags = self.request.query_params.get("tags")
            title = self.request.query_params.get("title")
            cover = self.request.query_params.get("cover")

            if authors:
                author_ids = self._params_to_ints(authors)
                queryset = queryset.filter(author__id__in=author_ids)

            if tags:
                tag_names = self._split_str_params(tags)
                queryset = queryset.filter(tags__name__in=tag_names)

            if title:
                queryset = queryset.filter(title__icontains=title)

            if cover:
                queryset = queryset.filter(cover=cover.upper())

            queryset.filter(inventory__gt=0)

        return queryset


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
