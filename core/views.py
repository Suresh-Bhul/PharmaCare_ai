from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@login_required
def dashboard(request):
    from apps.customer.models import Customer
    from apps.medicine.models import Medicine, MedicineBatch
    from apps.purchase.models import Purchase
    from apps.sales.models import Sales
    from apps.supplier.models import Supplier

    today = date.today()
    month_start = today.replace(day=1)

    todays_sales = Sales.objects.filter(created_at__date=today)
    month_sales = Sales.objects.filter(created_at__date__gte=month_start)

    low_stock_medicines = (
        Medicine.objects.annotate(total_stock=Sum("medicinebatch__quantity"))
        .filter(total_stock__lte=F("reorder_level"))
        .order_by("total_stock")[:6]
    )

    expiring_batches = (
        MedicineBatch.objects.select_related("medicine")
        .filter(
            expiry_date__gte=today,
            expiry_date__lte=today + timedelta(days=30),
            quantity__gt=0,
        )
        .order_by("expiry_date")[:6]
    )

    recent_sales = Sales.objects.select_related("customer").order_by("-created_at")[:8]

    context = {
        "todays_sales_count": todays_sales.count(),
        "todays_sales_total": sum(s.total for s in todays_sales),
        "month_sales_total": sum(s.total for s in month_sales),
        "total_medicines": Medicine.objects.count(),
        "total_customers": Customer.objects.count(),
        "total_suppliers": Supplier.objects.count(),
        "pending_purchases": Purchase.objects.filter(is_purchase_verified=False).count(),
        "low_stock_medicines": low_stock_medicines,
        "expiring_batches": expiring_batches,
        "recent_sales": recent_sales,
    }
    return render(request, "dashboard/index.html", context)


def custom_404(request, exception=None):
    return render(request, "errors/404.html", status=404)


def custom_500(request):
    return render(request, "errors/500.html", status=500)


def custom_403(request, exception=None):
    return render(request, "errors/403.html", status=403)
