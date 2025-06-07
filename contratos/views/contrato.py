from rest_framework import viewsets
from contratos.models import Contrato
from contratos.serializers import ContratoSerializer, ContratoListSerializer


class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all("-id")
    serializer_class = ContratoSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ContratoListSerializer
        return ContratoSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
