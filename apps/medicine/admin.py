from django.contrib import admin
from apps.medicine.models import Category, Medicine

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
        "selling_price",
        "status",
        "expiry_date",
    )

    list_filter = (
        "dosage_form",
        "status",
        "manufacture_date",
        "expiry_date",
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

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Basic Information", {
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
        ("Pricing", {
            "fields": (
                "purchase_price",
                "selling_price",
                "tax_rate",
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
                "manufacture_date",
                "expiry_date",
                "created_at",
                "updated_at",
            )
        }),
    )

admin.site.register(Category)