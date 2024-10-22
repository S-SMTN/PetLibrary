import stripe
from django.conf import settings
from django.db import connection
from django.http import HttpResponseBadRequest
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from stripe import SignatureVerificationError

from Payments.models import Payment
from Payments.serializers import PaymentSerializer
from PetLibrary.utils.paginations import ViewPagination
from Public.models import Library


class PaymentListRetrieveVewSet(ReadOnlyModelViewSet):
    queryset = Payment.objects.all().prefetch_related(
        "borrowing__books__author",
        "borrowing__user"
    )
    serializer_class = PaymentSerializer
    pagination_class = ViewPagination
    permission_classes = [IsAdminUser,]
    authentication_classes = (JWTAuthentication,)


class PaymentSuccessView(APIView):
    def get(self, request: Request) -> Response:
        return Response({
            "Response": f"Payment successful!"
        })


class PaymentCancelView(APIView):
    def get(self, request: Request) -> Response:
        return Response({
            "Response": "Payment cancelled. Please try again."
        })


class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(
        self,
        request: Request,
        *args,
        **kwargs
    ) -> HttpResponseBadRequest | Response:
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return HttpResponseBadRequest()
        except SignatureVerificationError:
            return HttpResponseBadRequest()

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            self.handle_successful_payment(session)

        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def handle_successful_payment(session):
        """Stripe has not multiple webhooks for test account, therefore I've had to implement search
        for session_id in multiple schemas for each tenant"""
        session_id = session.get('id')
        schemas = [
            library.subdomain
            for library
            in Library.objects.all()
        ]

        for schema in schemas:
            table_name = f'"{schema}"."Payments_payment"'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE {table_name}
                    SET "status" = 'PAID'
                    WHERE session_id = %s
                    """,
                    [session_id]
                )

                if cursor.rowcount > 0:
                    break
