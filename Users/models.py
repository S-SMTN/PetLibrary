from django.contrib.auth.models import AbstractUser
from django.db import models

from Public.models import Library


class User(AbstractUser):
    email = models.EmailField(unique=True)

    @property
    def full_name(self) -> str:
        return self.get_full_name()

    def __str__(self) -> str:
        return (
            f"{self.full_name} ({self.email}), "
        )
