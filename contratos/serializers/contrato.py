from rest_framework import serializers
from contratos.models import Contrato
from contratos.serializers.parcela import ParcelaSerializer


class ContratoSerializer(serializers.ModelSerializer):
    parcelas = ParcelaSerializer(many=True, read_only=True)

    class Meta:
        model = Contrato
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_by", "updated_at")
