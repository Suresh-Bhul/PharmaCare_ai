from django.urls import path

from apps.report import views

urlpatterns = [
    path("", views.report_dashboard, name="report_dashboard"),
]
