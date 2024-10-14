from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal

from Borrowings.models import Borrowing


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'

    class PaymentType(models.TextChoices):
        PAYMENT = 'PAYMENT', 'Payment'
        FINE = 'FINE', 'Fine'

    status = models.CharField(max_length=7, choices=PaymentStatus.choices)
    payment_type = models.CharField(max_length=7, choices=PaymentType.choices)
    borrowing = models.ForeignKey(to=Borrowing, on_delete=models.PROTECT)
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return (
            f"{self.payment_type} - ${self.money_to_pay} to {self.borrowing}"
        )
