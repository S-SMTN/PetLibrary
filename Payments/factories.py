from typing import List

import factory
from factory.django import DjangoModelFactory
from faker import Faker
from decimal import Decimal

from Borrowings.models import Borrowing
from Payments.models import Payment


fake = Faker()


def get_random_borrowing() -> List[Borrowing]:
    return list(Borrowing.objects.order_by('?')[:10])


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    status = factory.Iterator(
        [Payment.PaymentStatus.PENDING, Payment.PaymentStatus.PAID]
    )
    payment_type = factory.Iterator(
        [Payment.PaymentType.PAYMENT, Payment.PaymentType.FINE]
    )
    borrowing = factory.Iterator(get_random_borrowing())
    session_url = factory.LazyAttribute(lambda _: fake.url())
    session_id = factory.LazyAttribute(lambda _: fake.uuid4())
    money_to_pay = factory.LazyAttribute(
        lambda _: round(
            fake.pydecimal(
                left_digits=3,
                right_digits=2,
                positive=True,
                min_value=Decimal('0.01')
            ),
            2
        )
    )
