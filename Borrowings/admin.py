from django.contrib import admin

from Borrowings.models import Borrowing
from Library.admin import tenant_admin_site


@admin.register(Borrowing, site=tenant_admin_site)
class BorrowingAdmin(admin.ModelAdmin):
    search_fields = ["borrow_date", "book", "user"]
    list_display = [
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
        "display_books",
        "user"
    ]
    list_editable = [
        "expected_return_date",
        "actual_return_date",
    ]
    list_filter = [
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
        "user"
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related("user")
        queryset = queryset.prefetch_related("books__author")
        return queryset

    def display_books(self, obj):
        return ", ".join([str(book) for book in obj.books.all()])

    display_books.short_description = "Books"
