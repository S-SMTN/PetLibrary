from typing import List

import factory
from factory.django import DjangoModelFactory
from faker import Faker
from Books.models import Author, Book

fake = Faker()


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())


def get_random_author() -> List[Author]:
    existing_authors = list(Author.objects.all().order_by('?')[:10])

    while len(existing_authors) < 10:
        new_author = AuthorFactory()
        existing_authors.append(new_author)

    return existing_authors


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.LazyAttribute(lambda _: fake.sentence(nb_words=3)[:-1])
    author = factory.Iterator(get_random_author())
    cover = factory.Iterator([Book.CoverType.HARD, Book.CoverType.SOFT])
    inventory = factory.LazyAttribute(
        lambda _: fake.random_int(min=1, max=100)
    )
    daily_fee = factory.LazyAttribute(
        lambda _: round(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True), 2
        )
    )
