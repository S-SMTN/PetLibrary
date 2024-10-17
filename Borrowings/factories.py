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


def get_random_user() -> List[User]:
    user = get_user_model()

    existing_users = list(
        user.objects.exclude(is_staff=True).order_by('?')[:10]
    )

    if not existing_users:
        user = UserFactory()
        return user

    return random.choice(existing_users)


class BorrowingFactory(DjangoModelFactory):
    class Meta:
        model = Borrowing

    borrow_date = factory.LazyAttribute(lambda _: fake.date_time_this_year())
    expected_return_date = factory.LazyAttribute(lambda _: None)
    actual_return_date = factory.LazyAttribute(lambda _: None)
    user = factory.LazyAttribute(lambda _: get_random_user())

    @factory.post_generation
    def books(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for book in extracted:
                self.book.add(book)
        else:
            books = Book.objects.all().order_by('?')[:3]
            for book in books:
                self.books.add(book)