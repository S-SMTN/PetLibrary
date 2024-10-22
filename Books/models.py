from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ["name"]


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    tags = models.ManyToManyField(to=Tag, related_name="authors", blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]


    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}"

    def __str__(self) -> str:
        return self.full_name


class Book(models.Model):
    class Meta:
        ordering = ["title", "author"]

    class CoverType(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(to=Tag, related_name="books", blank=True)
    author = models.ForeignKey(
        to=Author,
        on_delete=models.PROTECT,
        related_name="books"
    )
    cover = models.CharField(max_length=4, choices=CoverType.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )

    def __str__(self) -> str:
        return f"{self.title}"
