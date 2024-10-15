from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = 'HARD', 'Hardcover'
        SOFT = 'SOFT', 'Softcover'

    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        to=Author,
        on_delete=models.PROTECT,
        related_name="books"
    )
    cover = models.CharField(max_length=4, choices=CoverType.choices)
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    daily_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"
