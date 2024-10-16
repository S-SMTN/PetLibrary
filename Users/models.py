from django.contrib.auth.models import AbstractUser
from django.db import models

from Public.models import Library


class User(AbstractUser):

    def __str__(self) -> str:
        return (
            f"{self.first_name} {self.last_name} ({self.email}), "
        )
