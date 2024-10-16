from django.contrib import admin

from Books.models import Author, Book
from Library.admin import tenant_admin_site


@admin.register(Author, site=tenant_admin_site)
class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name"
    ]


@admin.register(Book, site=tenant_admin_site)
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
