from typing import List

from django.db import transaction
from rest_framework import serializers

from Books.models import Book
from Books.serialaizers import BookNestedSerializer, BookSerializer
from Borrowings.models import Borrowing
from Users.serializers import UserNestedSerializer


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
        ]
        read_only_fields = ["actual_return_date", "user"]


class BorrowingCreateSerializer(BorrowingSerializer):

    def validate_books(self, books: List[Book]) -> List[Book]:
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


class BorrowingListSerializer(BorrowingSerializer):
    books = BookNestedSerializer(many=True, read_only=True)
    user = UserNestedSerializer(read_only=True)


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
