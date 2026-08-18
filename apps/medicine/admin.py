from django.contrib import admin
from apps.medicine.models import Category, Medicine, MedicineBatch

# Register your models here.
@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "generic_name",
        "brand_name",
        "medicine_code",
        "dosage_form",
        "strength",
        "reorder_level",
        "status",
        
    )

    list_filter = (
        "dosage_form",
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "generic_name",
        "brand_name",
        "medicine_code",
        "barcode",
    )

    ordering = ("name",)
    list_per_page = 25
    date_hierarchy = "created_at"

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Medicine Information", {
            "fields": (
                "name",
                "generic_name",
                "brand_name",
                "medicine_code",
                "barcode",
            )
        }),
        ("Medicine Details", {
            "fields": (
                "dosage_form",
                "strength",
                "status",
            )
        }),
     
        ("Inventory", {
            "fields": (
                "reorder_level",
                "storage_location",
                "category",
            )
        }),

        ("Dates", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

admin.site.register(Category)


@admin.register(MedicineBatch)
class MedicineBatchAdmin(admin.ModelAdmin):
    list_display = (
        "medicine",
        "batch_number",
        "supplier",
        "quantity",
        "purchase_price",
        "selling_price",
        "manufacturing_date",
        "expiry_date",
        "received_date",
        "status",
    )

    list_filter = (
        "status",
        "supplier",
        "expiry_date",
        "received_date",
    )

    search_fields = (
        "medicine__name",
        "batch_number",
        "supplier__name",
    )

    list_editable = (
        "quantity",
        "selling_price",
        "status",
    )


    ordering = (
        "-received_date",
        "medicine",
        "batch_number",
    )

    date_hierarchy = "received_date"

    fieldsets = (
        (
            "Medicine & Batch",
            {
                "fields": (
                    "medicine",
                    "batch_number",
                    "supplier",
                )
            },
        ),
        (
            "Stock & Pricing",
            {
                "fields": (
                    "quantity",
                    "purchase_price",
                    "selling_price",
                    "status",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "manufacturing_date",
                    "expiry_date",
                    "received_date",
                )
            },
        ),
    )