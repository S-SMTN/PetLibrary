from django.db.models import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet

from Books.factories import BookFactory
from Books.models import Author, Book
from Books.serialaizers import AuthorSerializer, BookSerializer
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
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(AdminOrAuthenticatedReadOnlyViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self) -> QuerySet:
        if self.action == "list":
            return self.queryset.select_related("author")

