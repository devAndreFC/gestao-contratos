from rest_framework import serializers
from contratos.models import Contrato, Parcela
from contratos.serializers.parcela import ParcelaSerializer


class ContratoSerializer(serializers.ModelSerializer):
    parcelas = ParcelaSerializer(many=True, required=False)

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
            "cpf",
            "pais",
            "estado",
            "cidade",
            "numero_telefone",
            "taxa_contrato",
            "parcelas",
        )
        read_only_fields = ("created_by", "created_at", "updated_by", "updated_at")

    def create(self, validated_data):
        parcelas_data = validated_data.pop("parcelas", [])
        contrato = Contrato.objects.create(**validated_data)
        created_by = validated_data["created_by"]
        for parcela_data in parcelas_data:
            Parcela.objects.create(
                contrato=contrato,
                created_by=created_by,
                **parcela_data,
            )
        return contrato

    def update(self, instance, validated_data):
        parcelas_data = validated_data.pop("parcelas", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if parcelas_data is not None:
            instance.parcelas.all().delete()
            for parcela_data in parcelas_data:
                Parcela.objects.create(contrato=instance, **parcela_data)

        return instance


class ContratoListSerializer(serializers.HyperlinkedModelSerializer):
    total_parcelas = serializers.SerializerMethodField()

    class Meta:
        model = Contrato
        fields = (
            "url",
            "id",
            "data_emissao",
            "cpf",
            "valor_desembolsado",
            "taxa_contrato",
            "total_parcelas",
        )

    def get_total_parcelas(self, obj):
        return obj.parcelas.count()


class ContratoResumoSerializer(serializers.Serializer):
    valor_total_a_receber = serializers.FloatField()
    valor_total_desembolsado = serializers.FloatField()
    numero_total_contratos = serializers.IntegerField()
    taxa_media = serializers.FloatField()
