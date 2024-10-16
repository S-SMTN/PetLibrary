from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from Books.factories import BookFactory
from Books.models import Author, Book
from Books.serialaizers import AuthorSerializer, BookSerializer
from PetLibrary.utils.paginations import ViewPagination
from PetLibrary.utils.permissions import IsAdminOrIfAuthenticatedReadOnly


def factory_book(request):
    books = [BookFactory() for _ in range(10)]

    return HttpResponse(f"{[str(book) for book in books]}")


class AdminOrAuthenticatedReadOnlyViewSet(ModelViewSet):
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

