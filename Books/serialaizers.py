from decimal import Decimal

from rest_framework import serializers

from Books.models import Book, Author, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TagNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class AuthorListSerializer(serializers.ModelSerializer):
    tags = TagNestedSerializer(many=True)

    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "full_name", "tags"]


class AuthorCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "full_name", "tags"]

    def create(self, validated_data: dict) -> Author:
        tags = validated_data.pop("tags")
        author = Author.objects.create(**validated_data)
        for tag in tags:
            author.tags.add(tag)
        return author

    def update(self, instance: Author, validated_data: dict) -> Author:
        tags = validated_data.pop("tags", [])

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()

        if tags:
            instance.tags.clear()
            for tag in tags:
                instance.tags.add(tag)

        return instance


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ["id", "title", "tags", "author", "cover", "inventory", "daily_fee"]

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


class BookListSerializer(BookSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="full_name"
    )
    tags = TagNestedSerializer(many=True)


class BookCreateUpdateSerializer(BookSerializer):

    def create(self, validated_data: dict) -> Book:
        tags = validated_data.pop("tags", [])
        book = Book.objects.create(**validated_data)
        for tag in tags:
            book.tags.add(tag)
        return book

    def update(self, instance: Author, validated_data: dict) -> Author:
        tags = validated_data.pop("tags", [])

        instance.title = validated_data.get("title", instance.title)
        instance.author = validated_data.get("author", instance.author)
        instance.cover = validated_data.get("cover", instance.cover)
        instance.inventory = validated_data.get("inventory", instance.inventory)
        instance.daily_fee = validated_data.get("daily_fee", instance.daily_fee)
        instance.save()

        if tags:
            instance.tags.clear()
            for tag in tags:
                instance.tags.add(tag)

        return instance


class BookNestedSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="full_name"
    )

    class Meta:
        model = Book
        fields = ["title", "author", "daily_fee"]
