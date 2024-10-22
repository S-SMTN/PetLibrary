from datetime import date
from decimal import Decimal

import stripe
from django.conf import settings
from django.urls import reverse_lazy
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from stripe import StripeError
from stripe.checkout import Session

from Borrowings.models import Borrowing

stripe.api_key = settings.STRIPE_SECRET_KEY


def calculate_total_price(borrowing: Borrowing) -> Decimal:
    borrow_days = (borrowing.expected_return_date - borrowing.borrow_date).days
    if borrow_days <= 0:
        borrow_days = 1

    total_price = sum([book.daily_fee * borrow_days for book in borrowing.books.all()])
    return total_price


def calculate_fine(borrowing: Borrowing) -> Decimal:
    today = date.today()
    expected_return_date = borrowing.expected_return_date.date()

    if today > expected_return_date:
        fine_days = (today - expected_return_date).days
        total_fine = sum([
            float(book.daily_fee * fine_days) * 1.5
            for book in borrowing.books.all()
        ])
        return total_fine


def create_stripe_payment_session(
        borrowing: Borrowing,
        request: Request,
        total_price: Decimal,
) -> Session:
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Borrowing #{borrowing.id}",
                    },
                    "unit_amount": int(total_price * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=request.build_absolute_uri(reverse_lazy("payments:success")),
            cancel_url=request.build_absolute_uri(reverse_lazy("payments:cancel")),
        )

        return session
    except StripeError as e:
        raise APIException(e)
