from datetime import datetime
from typing import List

from django.db import transaction
from django.utils import timezone
from django.utils.timezone import is_aware, make_aware
from rest_framework import serializers

from Books.models import Book
from Books.serialaizers import BookNestedSerializer
from Borrowings.models import Borrowing
from Users.serializers import UserNestedSerializer


class MetaBase:
    model = Borrowing
    fields = [
        "id",
        "books",
        "user",
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
    ]
    read_only_fields = ["actual_return_date", "user"]


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "books",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "payments"
        ]
        read_only_fields = ["actual_return_date", "user"]

    def validate(self, attrs: dict) -> dict:
        borrow_date = attrs.get("borrow_date", datetime.now())
        expected_return_date = attrs.get("expected_return_date")

        if expected_return_date and not is_aware(expected_return_date):
            expected_return_date = make_aware(expected_return_date)
        if borrow_date and not is_aware(borrow_date):
            borrow_date = make_aware(borrow_date)

        if expected_return_date and expected_return_date <= borrow_date:
            raise serializers.ValidationError(
                {"expected_return_date": "Expected return date must be after the borrow date."}
            )
        return attrs

    @staticmethod
    def validate_books(books: List[Book]) -> List[Book]:
        for book in books:
            if book.inventory == 0:
                raise serializers.ValidationError(
                    f"Book '{book}' is not available for borrowing. Inventory is 0."
                )
        return books

    def create(self, validated_data: dict) -> Borrowing:
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user

        books = validated_data.pop("books")

        with transaction.atomic():
            borrowing: Borrowing = Borrowing.objects.create(**validated_data)
            borrowing.books.set(books)

            for book in books:
                book.inventory -= 1
                book.save()

            return borrowing


class BorrowingUpdateSerializer(BorrowingListSerializer):
    class Meta(MetaBase):
        read_only_fields = MetaBase.read_only_fields.extend([
            "id",
            "books",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        ])


    @staticmethod
    def validate_borrowing(borrowing: Borrowing):
        if borrowing.actual_return_date is not None:
            raise serializers.ValidationError(
                "This borrowing is already returned!"
            )

    def update(self, instance: Borrowing, validated_data: dict) -> Borrowing:
        self.validate_borrowing(instance)

        with transaction.atomic():
            for book in instance.books.all():
                book.inventory += 1
                book.save()

            instance.actual_return_date = timezone.now()
            instance.save()

        return instance


class BorrowingFactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "books",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        ]
