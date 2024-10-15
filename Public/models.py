from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.core.exceptions import ValidationError

import re


class LibraryTenant(TenantMixin):
    name = models.CharField(max_length=40)


class Domain(DomainMixin):
    pass


class Library(models.Model):
    name = models.CharField(max_length=40)
    subdomain = models.CharField(max_length=40)
    address = models.TextField()

    def clean(self) -> None:
        self.validate_subdomain()

    def validate_subdomain(self) -> None:
        if not re.match(r'^[a-zA-Z0-9-]+$', self.subdomain):
            raise ValidationError("Subdomain can only contain alphanumeric characters and hyphens.")

        if self.subdomain.startswith('-') or self.subdomain.endswith('-'):
            raise ValidationError("Subdomain cannot start or end with a hyphen.")

        if len(self.subdomain) < 3 or len(self.subdomain) > 63:
            raise ValidationError("Subdomain must be between 3 and 63 characters long.")

    def save(self, *args, **kwargs) -> None:
        self.subdomain = self.subdomain.strip().lower()
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.subdomain})"
