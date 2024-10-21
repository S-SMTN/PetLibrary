from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from Payments.models import Payment
from Payments.serializers import PaymentSerializer
from PetLibrary.utils.paginations import ViewPagination


class PaymentListRetrieveVewSet(ReadOnlyModelViewSet):
    queryset = Payment.objects.all().prefetch_related(
        "borrowing__books__author",
        "borrowing__user"
    )
    serializer_class = PaymentSerializer
    pagination_class = ViewPagination
    permission_classes = [IsAdminUser,]
    authentication_classes = (JWTAuthentication,)
