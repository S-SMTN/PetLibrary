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

    class Meta:
        ordering = ["-created_at"]

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=7, choices=PaymentStatus.choices)
    payment_type = models.CharField(max_length=7, choices=PaymentType.choices)
    borrowing = models.ForeignKey(to=Borrowing, on_delete=models.PROTECT, related_name="payments")
    session_url = models.URLField(max_length=500)
    session_id = models.TextField()
    money_to_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.payment_type} - ${self.money_to_pay} to {self.borrowing}"
        )
