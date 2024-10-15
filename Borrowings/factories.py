import random

import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.contrib.auth import get_user_model
from Books.models import Book
from .models import Borrowing


fake = Faker()


def get_random_user():
    user = get_user_model()
    existing_users = list(
        user.objects.exclude(is_staff=True).order_by('?')[:10]
    )

    return random.choice(existing_users)


class BorrowingFactory(DjangoModelFactory):
    class Meta:
        model = Borrowing

    borrow_date = factory.LazyAttribute(lambda _: fake.date_time_this_year())
    expected_return_date = factory.LazyAttribute(lambda _: None)
    actual_return_date = factory.LazyAttribute(lambda _: None)
    book = factory.Iterator(Book.objects.all())
    user = factory.LazyAttribute(lambda _: get_random_user())
