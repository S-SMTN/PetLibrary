from django.urls import path, include
from rest_framework import routers

from Books.views import AuthorViewSet, BookViewSet, TagViewSet

book_router = routers.DefaultRouter()
book_router.register(prefix="authors", viewset=AuthorViewSet)
book_router.register(prefix="books", viewset=BookViewSet)
book_router.register(prefix="tags", viewset=TagViewSet)

urlpatterns = [path("", include(book_router.urls))]

app_name = "books"
