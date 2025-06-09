from rest_framework import viewsets
from contratos.models import Contrato
from contratos.serializers import (
    ContratoSerializer,
    ContratoListSerializer,
    ContratoResumoSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from contratos.filters import ContratosFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from contratos.services import ContratoResumoService


class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all().order_by("-id")
    serializer_class = ContratoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContratosFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ContratoListSerializer
        return ContratoSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(detail=False, methods=["get"], url_path="resumo")
    def resumo(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        resumo_data = ContratoResumoService.gerar_resumo(queryset)
        serializer = ContratoResumoSerializer(resumo_data)
        return Response(serializer.data)
