from django.urls import path, include
from rest_framework.routers import DefaultRouter
from contratos.views import ContratoViewSet, ParcelaViewSet

router = DefaultRouter()
router.register(r"contratos", ContratoViewSet)
router.register(r"parcelas", ParcelaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
