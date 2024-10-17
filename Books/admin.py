from django.contrib import admin

from Books.models import Author, Book
from Library.admin import tenant_admin_site


@admin.register(Author, site=tenant_admin_site)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name"]
    list_display = [
        "first_name",
        "last_name"
    ]


@admin.register(Book, site=tenant_admin_site)
class BookAdmin(admin.ModelAdmin):
    search_fields = ["title", "author"]
    list_display = [
        "id",
        "title",
        "author",
        "cover",
        "inventory",
        "daily_fee"
    ]
    list_editable = [
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
