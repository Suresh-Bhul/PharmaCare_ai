from datetime import date, timedelta

def pharmacy_alerts(request):
    """
    Adds low-stock and near-expiry counters to every template's context so the
    navbar notification bell can show a live badge without every view having
    to remember to pass it in.
    """
    if not request.user.is_authenticated:
        return {}

    from django.db.models import F, Sum
    from apps.medicine.models import Medicine, MedicineBatch

    try:
        low_stock_count = (
            Medicine.objects.annotate(total_stock=Sum("medicinebatch__quantity"))
            .filter(total_stock__lte=F("reorder_level"))
            .count()
        )
        expiring_soon_count = MedicineBatch.objects.filter(
            expiry_date__gte=date.today(),
            expiry_date__lte=date.today() + timedelta(days=30),
            quantity__gt=0,
        ).count()
        expired_count = MedicineBatch.objects.filter(
            expiry_date__lt=date.today(), quantity__gt=0
        ).count()
    except Exception:
        # Fails gracefully before migrations/tables exist (e.g. during manage.py check)
        low_stock_count = expiring_soon_count = expired_count = 0

    return {
        "alert_low_stock_count": low_stock_count,
        "alert_expiring_soon_count": expiring_soon_count,
        "alert_expired_count": expired_count,
        "alert_total_count": low_stock_count + expiring_soon_count + expired_count,
    }

