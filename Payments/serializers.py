from rest_framework import serializers

from Borrowings.serializers import BorrowingListSerializer
from Payments.models import Payment


class PaymentSerializer(serializers.Serializer):
    borrowing = BorrowingListSerializer
    class Meta:
        model: Payment
        fields = [
            "status",
            "payment_type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay"
        ]
