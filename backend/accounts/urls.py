"""Rotas públicas responsáveis por autenticação."""

from django.urls import path

from accounts.views import LoginView, LogoutView, ProfileView, RefreshView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="accounts-register"),
    path("login/", LoginView.as_view(), name="accounts-login"),
    path("refresh/", RefreshView.as_view(), name="accounts-refresh"),
    path("me/", ProfileView.as_view(), name="accounts-profile"),
    path("logout/", LogoutView.as_view(), name="accounts-logout"),
]
