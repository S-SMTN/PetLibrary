from django.urls import path

from Borrowings.views import factory_borrowing
from Library.admin import tenant_admin_site

from Library.views import index

from Books.views import factory_book

urlpatterns = [
    path('admin/', tenant_admin_site.urls),
    path("", index),
    path("factory_book/", factory_book),
    path("factory_borrowing/", factory_borrowing)
]
