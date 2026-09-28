from django.urls import path

from apps.report.views import report_dashboard

urlpatterns = [
    path("", report_dashboard, name="report_dashboard"),
]
