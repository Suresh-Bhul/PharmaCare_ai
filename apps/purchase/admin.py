from django.contrib import admin

from apps.purchase.models import Purchase, PurchaseItem

# Register your models here.
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "purchase_number",
        "supplier",
        "purchase_date",
        "invoice_number",
        "subtotal",
        "discount",
        "tax",
        "total",
        "payment_status",
        "created_at",
    )

    list_filter = (
        "payment_status",
        "purchase_date",
        "created_at",
    )

    search_fields = (
        "purchase_number",
        "invoice_number",
        "supplier",
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = (
        "purchase",
        "medicine",
        "batch_number",
        "manufacturing_date",
        "expiry_date",
        "quantity",
        "unit_price",
        "discount",
        "tax",
        "total",
    )

    list_filter = (
        "manufacturing_date",
        "expiry_date",
    )

    search_fields = (
        "batch_number",
        "purchase__purchase_number",
        "medicine__name",
    )