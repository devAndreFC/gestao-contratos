from rest_framework import viewsets
from contratos.models import Contrato
from contratos.serializers import ContratoSerializer, ContratoListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from contratos.filters import ContratosFilter

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
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
