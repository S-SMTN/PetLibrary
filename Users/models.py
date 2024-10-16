from django.contrib.auth.models import AbstractUser
from django.db import models

from Public.models import Library


class User(AbstractUser):
    library = models.ForeignKey(
        Library,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    def __str__(self) -> str:
        return (
            f"{self.first_name} {self.last_name} ({self.email}), "
            f"library: {self.library}"
        )
