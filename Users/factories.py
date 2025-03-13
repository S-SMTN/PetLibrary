import factory
from factory import LazyAttribute
from faker import Faker
from django.contrib.auth import get_user_model

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = LazyAttribute(lambda _: fake.first_name())
    last_name = LazyAttribute(lambda _: fake.last_name())
    email = LazyAttribute(lambda _: fake.email())
    username = LazyAttribute(lambda _: fake.user_name())
    password = factory.PostGenerationMethodCall('set_password', 'password')
