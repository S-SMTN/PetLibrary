from django.contrib import admin

from Borrowings.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    search_fields = ["borrow_date", "book", "user"]
    list_display = [
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
        "book",
        "user"
    ]
    list_editable = [
        "expected_return_date",
        "actual_return_date",
        "book",
        "user"
    ]
    list_filter = [
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
        "book",
        "user"
    ]
