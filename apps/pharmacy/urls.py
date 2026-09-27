from django.urls import path

from apps.pharmacy import views

urlpatterns = [
    path("", views.pharmacy_settings, name="pharmacy_settings"),
]
