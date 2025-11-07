"""Rotas de Reservas."""

from rest_framework.routers import DefaultRouter

from reservations.views import ReservationViewSet

router = DefaultRouter()
router.register(r"reservations", ReservationViewSet, basename="reservation")

urlpatterns = router.urls
