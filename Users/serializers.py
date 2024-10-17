from rest_framework import serializers


from Users.models import User


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name", "email"]
