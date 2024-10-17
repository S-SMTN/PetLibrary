from rest_framework import serializers

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


class BorrowingListSerializer(BorrowingSerializer):
    books = BookNestedSerializer(many=True, read_only=True)
    user = UserNestedSerializer(read_only=True)
