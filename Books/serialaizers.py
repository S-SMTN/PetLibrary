from decimal import Decimal

from rest_framework import serializers

from Books.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "full_name"]


class AuthorNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["full_name"]


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="full_name"
    )

    class Meta:
        model = Book
        fields = ["id", "title", "author", "cover", "inventory", "daily_fee"]

    @staticmethod
    def validate_cover(value):
        if value not in [Book.CoverType.HARD, Book.CoverType.SOFT]:
            raise serializers.ValidationError("Invalid cover type. Must be 'HARD' or 'SOFT'.")
        return value

    @staticmethod
    def validate_inventory(value):
        if value < 0:
            raise serializers.ValidationError("Inventory cannot be less than 0.")
        return value

    @staticmethod
    def validate_daily_fee(value):
        if value < Decimal("0.01"):
            raise serializers.ValidationError("Daily fee cannot be less than 0.01.")
        return value
