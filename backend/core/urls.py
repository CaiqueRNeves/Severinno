"""Rotas do app core."""

from django.urls import path

from core.views import HealthCheckView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
]
