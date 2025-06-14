from rest_framework import serializers
from contratos.models import Parcela


class ParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcela
        fields = "__all__"
        extra_kwargs = {
            "contrato": {"required": False},
            "created_by": {"read_only": True},
            "updated_by": {"read_only": True},
        }
