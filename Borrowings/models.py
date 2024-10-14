from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

from Books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateTimeField(auto_now_add=True)
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(to=Book, on_delete=models.PROTECT)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

    @property
    def expected_return_date(self):
        return self.borrow_date + timedelta(days=30)

    def __str__(self):
        return f"Borrowing of {self.book} by {self.user}"
