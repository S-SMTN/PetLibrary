from django.http import HttpResponse
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from Users.factories import UserFactory
from Users.models import User
from Users.serializers import UserSerializer


def factory_user(request):
    users = UserFactory.create_batch(10)

    return HttpResponse(f"{[str(user) for user in users]}")


class UserBaseView:
    serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(
    UserBaseView,
    generics.RetrieveUpdateAPIView
):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user
