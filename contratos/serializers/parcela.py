from rest_framework import serializers
from contratos.models import Parcela


class ParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcela
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_by", "updated_at")
