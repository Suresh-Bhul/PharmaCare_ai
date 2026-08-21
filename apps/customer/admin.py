from django.contrib import admin

from apps.customer.models import Customer

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "email",
        "date_of_birth",
        "gender",
        "status",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "gender",
        "status",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "email",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "full_name",
                    "date_of_birth",
                    "gender",
                )
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "phone",
                    "email",
                    "address",
                    "emergency_contact",
                )
            },
        ),
        (
            "Account Information",
            {
                "fields": (
                    "status",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )