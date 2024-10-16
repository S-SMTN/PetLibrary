from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Users.models import User


@admin.register(User)
class WorkerAdmin(UserAdmin):
    search_fields = ["email", "first_name", "last_name", "library"]
    list_filter = ["email", "first_name", "last_name", "library"]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "library"
    ]
    list_editable = ["is_staff", "library"]