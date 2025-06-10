import django_filters
from datetime import datetime
from contratos.models import Contrato


class ContratosFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name="id", lookup_expr="exact")
    cpf = django_filters.CharFilter(field_name="cpf", lookup_expr="exact")
    estado = django_filters.CharFilter(field_name="estado", lookup_expr="iexact")

    data = django_filters.CharFilter(method="filter_data")

    class Meta:
        model = Contrato
        fields = ["id", "cpf", "data", "estado"]

    def filter_data(self, queryset, name, value):
        try:
            data = datetime.strptime(value, "%m/%Y")
            return queryset.filter(
                data_emissao__year=data.year,
                data_emissao__month=data.month,
            )
        except ValueError:
            pass

        try:
            data = datetime.strptime(value, "%Y")
            return queryset.filter(data_emissao__year=data.year)
        except ValueError:
            pass
        return queryset
