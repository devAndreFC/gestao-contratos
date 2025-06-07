from rest_framework import serializers
from contratos.models import Contrato
from contratos.serializers.parcela import ParcelaSerializer


class ContratoSerializer(serializers.ModelSerializer):
    parcelas = ParcelaSerializer(many=True, read_only=True)

    class Meta:
        model = Contrato
        fields = (
            "id",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
            "data_emissao",
            "data_nascimento_tomador",
            "valor_desembolsado",
            "numero_documento",
            "pais",
            "estado",
            "cidade",
            "numero_telefone",
            "taxa_contrato",
            "parcelas",
        )
        read_only_fields = ("created_by", "created_at", "updated_by", "updated_at")


class ContratoListSerializer(serializers.ModelSerializer):
    total_parcelas = serializers.SerializerMethodField()

    class Meta:
        model = Contrato
        fields = (
            "id",
            "data_emissao",
            "numero_documento",
            "valor_desembolsado",
            "taxa_contrato",
            "total_parcelas",
        )

    def get_total_parcelas(self, obj):
        return obj.parcelas.count()
