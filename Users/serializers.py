from django.contrib.auth import get_user_model
from rest_framework import serializers


from Users.models import User


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name", "email"]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password"
        )
        read_only_fields = ("id",)
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"}
            }
        }

    def create(self, validated_data: dict) -> User:
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop("password", None)
        user = super().update(
            instance=instance,
            validated_data=validated_data
        )
        if password:
            user.set_password(password)
            user.save()

        return user
