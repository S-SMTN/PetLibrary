from typing import Type

from rest_framework import mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from Public.models import Library
from Public.serializers import LibrarySerializer, LibraryUpdateSerializer


class LibraryViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    permission_classes = [IsAdminUser,]
    authentication_classes = (JWTAuthentication,)
    queryset = Library.objects.all()

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "update":
            return LibraryUpdateSerializer
        return LibrarySerializer
