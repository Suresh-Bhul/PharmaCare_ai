from django.contrib import admin
from .models import District, Pharmacy

# Register your models here.


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = (
        "district_id",
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "district_id",
    )


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "registration_number",
        "email",
        "phone",
        "city",
        "district",
        "opening_time",
        "closing_time",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "district",
        "created_at",
    )

    search_fields = (
        "name",
        "registration_number",
        "email",
        "phone",
        "city",
    )

    autocomplete_fields = (
        "district",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    ordering = (
        "name",
    )

