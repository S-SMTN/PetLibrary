from rest_framework import serializers

from Public.models import Library


class MetaBase:
    model = Library
    fields = ["id", "name", "subdomain", "address", "created_at"]


class LibrarySerializer(serializers.ModelSerializer):
    class Meta(MetaBase):
        pass


class LibraryUpdateSerializer(serializers.ModelSerializer):
    class Meta(MetaBase):
        read_only_fields = ["subdomain"]
