from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Users.models import User


@admin.register(User)
class WorkerAdmin(UserAdmin):
    search_fields = ["email", "first_name", "last_name"]
    list_filter = ["email", "first_name", "last_name"]
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "username",
                        "email"
                    )
                },
            ),
        )
    )