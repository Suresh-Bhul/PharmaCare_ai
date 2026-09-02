from django.contrib import admin
from apps.inventory.models import InventoryTxn

# Register your models here.
@admin.register(InventoryTxn)
class InventoryTxnAdmin(admin.ModelAdmin):
    list_display = (
        "batch",
        "transaction_type",
        "quantity",
        "previous_stock",
        "new_stock",
        "reference_id",
        "created_at",
    )

    list_filter = (
        "transaction_type",
        "created_at",
    )

    search_fields = (
        "batch__medicine__name",
        "batch__batch_number",
        "reference_id",
    )

    # readonly_fields = (
    #     "batch",
    #     "transaction_type",
    #     "quantity",
    #     "reference_id",
    #     "previous_stock",
    #     "new_stock",
    #     "created_at",
    # )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"
