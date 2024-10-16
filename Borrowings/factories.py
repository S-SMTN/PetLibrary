import random
from typing import List

import factory
from django_tenants.utils import tenant_context
from factory.django import DjangoModelFactory
from faker import Faker
from django.contrib.auth import get_user_model
from Books.models import Book
from Public.models import Library
from Users.factories import UserFactory
from Users.models import User
from .models import Borrowing


fake = Faker()


def get_tenant_library(tenant: str) -> Library:
    if not tenant:
        raise ValueError("Tenant must be provided")

    return Library.objects.get(subdomain=tenant)


def get_random_user(tenant: str) -> List[User]:
    user = get_user_model()
    library = get_tenant_library(tenant)

    existing_users = list(
        user.objects.filter(library=library)
        .exclude(is_staff=True).order_by('?')[:10]
    )

    if not existing_users:
        user = UserFactory()
        user.library = library
        user.save()
        return user

    return random.choice(existing_users)


class BorrowingFactory(DjangoModelFactory):
    class Meta:
        model = Borrowing

    borrow_date = factory.LazyAttribute(lambda _: fake.date_time_this_year())
    expected_return_date = factory.LazyAttribute(lambda _: None)
    actual_return_date = factory.LazyAttribute(lambda _: None)
    book = factory.Iterator(Book.objects.all())

    @factory.lazy_attribute
    def user(self):
        return get_random_user(self.tenant)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        tenant = kwargs.pop('tenant', None)
        if not tenant:
            raise ValueError("Tenant must be provided")
        with tenant_context(tenant):
            return super()._create(model_class, *args, **kwargs)