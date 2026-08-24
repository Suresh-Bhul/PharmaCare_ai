from django.contrib import admin

from apps.sales.models import Sales, SalesItem

# Register your models here.
@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "customer",
        "sub_total",
        "discount",
        "tax",
        "total",
        "payment_status",
        "payment_method",
        "created_at",
    )

    list_filter = (
        "payment_status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "invoice_number",
        "customer__name",
    )

    readonly_fields = ("created_at",)

    ordering = ("-created_at",)


@admin.register(SalesItem)
class SalesItemAdmin(admin.ModelAdmin):
    list_display = (
        "sale",
        "medicine",
        "batch",
        "quantity",
        "unit_price",
        "discount",
        "tax",
        "total",
    )

    list_filter = (
        "medicine",
        "batch",
    )

    search_fields = (
        "sale__invoice_number",
        "medicine__name",
    )

    autocomplete_fields = ["sale", "medicine", "batch"]
