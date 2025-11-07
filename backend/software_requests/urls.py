"""Rotas do módulo de solicitações de software."""

from rest_framework.routers import DefaultRouter

from software_requests.views import SoftwareRequestViewSet

router = DefaultRouter()
router.register(r"software-requests", SoftwareRequestViewSet, basename="software-request")

urlpatterns = router.urls
