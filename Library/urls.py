from django.urls import path, include

from Borrowings.views import BorrowingFactoryView
from Library.admin import tenant_admin_site

from Books.views import BookFactoryView

urlpatterns = [
    path("admin/", tenant_admin_site.urls),
    path("api/book_factory/", BookFactoryView.as_view()),
    path("api/borrowing_factory/", BorrowingFactoryView.as_view()),
    path(
        "api/books/", include("Books.urls", namespace="books")
    ),
    path(
        "api/borrowings/", include("Borrowings.urls", namespace="borrowings")
    ),
    path(
        "api/payments/", include("Payments.urls", namespace="payments")
    )
]
