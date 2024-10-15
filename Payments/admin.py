from django.contrib import admin

from Payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "status",
        "payment_type",
        "borrowing",
        "session_url",
        "session_id",
        "money_to_pay"
    ]
    list_filter = [
        "status",
        "payment_type",
        "borrowing",
        "session_url",
        "session_id",
        "money_to_pay"
    ]
    readonly_fields = [field.name for field in Payment._meta.fields]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
