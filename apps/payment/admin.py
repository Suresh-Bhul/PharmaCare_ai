from django.contrib import admin

from apps.payment.models import PaymentLog

# Register your models here.
@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = (
        "sale",
        "transaction_id",
        "pidx",
        "amount",
        "currency",
        "status",
        "gateway_response",
        "verified_at",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "currency",
        "gateway_response",
        "created_at",
        "verified_at",
    )

    search_fields = (
        "transaction_id",
        "pidx",
        "sale__id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "verified_at",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    fieldsets = (
        (
            "Payment Information",
            {
                "fields": (
                    "sale",
                    "transaction_id",
                    "pidx",
                    "amount",
                    "currency",
                    "status",
                    "gateway_response",
                )
            },
        ),
        (
            "Verification",
            {
                "fields": (
                    "verified_at",
                )
            },
        ),
        (
            "System Info",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
