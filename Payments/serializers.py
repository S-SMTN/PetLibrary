from rest_framework import serializers
from Payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "id",
            "created_at",
            "status",
            "payment_type",
            "session_url",
            "session_id",
            "money_to_pay",
        ]
