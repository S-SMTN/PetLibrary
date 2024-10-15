from django.contrib import admin

from Books.models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name"
    ]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ["title", "author"]
    list_display = [
        "title",
        "author",
        "cover",
        "inventory",
        "daily_fee"
    ]
    list_editable = [
        "author",
        "cover",
        "inventory",
        "daily_fee"
    ]
    list_filter = [
        "title",
        "author",
        "cover",
        "inventory",
        "daily_fee"
    ]
