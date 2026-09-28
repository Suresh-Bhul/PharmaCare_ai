from django.shortcuts import render
import json
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.db.models.functions import TruncDate

# Create your views here.
@login_required
def report_dashboard(request):
    from apps.medicine.models import Medicine, MedicineBatch
    from apps.purchase.models import Purchase
    from apps.sales.models import Sales, SalesItem

    today = date.today()
    range_start = today - timedelta(days=29)

    # Sales trend for the last 30 days
    daily_sales = (
        Sales.objects.filter(created_at__date__gte=range_start)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Sum("total"))
        .order_by("day")
    )
    sales_by_day = {row["day"]: float(row["total"] or 0) for row in daily_sales}
    trend_labels = [(range_start + timedelta(days=i)).strftime("%b %d") for i in range(30)]
    trend_values = [sales_by_day.get(range_start + timedelta(days=i), 0) for i in range(30)]

    # Top selling medicines (by quantity) in the last 30 days
    top_medicines = (
        SalesItem.objects.filter(sale__created_at__date__gte=range_start)
        .values("medicine__name")
        .annotate(qty_sold=Sum("quantity"), revenue=Sum("total"))
        .order_by("-qty_sold")[:8]
    )

    # Low stock + expiring batches
    low_stock = (
        Medicine.objects.annotate(total_stock=Sum("medicinebatch__quantity"))
        .filter(total_stock__lte=F("reorder_level"))
        .order_by("total_stock")[:10]
    )
    expiring = (
        MedicineBatch.objects.select_related("medicine")
        .filter(expiry_date__gte=today, expiry_date__lte=today + timedelta(days=60), quantity__gt=0)
        .order_by("expiry_date")[:10]
    )

    # Purchase summary
    purchases_30d = Purchase.objects.filter(created_at__date__gte=range_start)
    total_purchase_value = purchases_30d.aggregate(total=Sum("total"))["total"] or 0

    total_sales_value = sum(trend_values)

    context = {
        "trend_labels": json.dumps(trend_labels),
        "trend_values": json.dumps(trend_values),
        "top_medicine_labels": json.dumps([m["medicine__name"] for m in top_medicines]),
        "top_medicine_values": json.dumps([m["qty_sold"] for m in top_medicines]),
        "top_medicines": top_medicines,
        "low_stock": low_stock,
        "expiring": expiring,
        "total_sales_value": total_sales_value,
        "total_purchase_value": total_purchase_value,
        "purchase_count_30d": purchases_30d.count(),
        "range_start": range_start,
        "range_end": today,
    }
    return render(request, "reports/dashboard.html", context)
