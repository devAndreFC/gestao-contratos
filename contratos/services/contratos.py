from django.db.models import Sum, Avg
from contratos.models import Parcela, Contrato

class ContratoResumoService:
    @staticmethod
    def gerar_resumo(queryset):
        valor_total_a_receber = Parcela.objects.filter(
            contrato__in=queryset
        ).aggregate(total=Sum("valor_parcela"))["total"] or 0

        valor_total_desembolsado = queryset.aggregate(
            total=Sum("valor_desembolsado")
        )["total"] or 0

        numero_total_contratos = queryset.count()

        taxa_media = queryset.aggregate(
            media=Avg("taxa_contrato")
        )["media"] or 0

        return {
            "valor_total_a_receber": float(valor_total_a_receber),
            "valor_total_desembolsado": float(valor_total_desembolsado),
            "numero_total_contratos": numero_total_contratos,
            "taxa_media": float(taxa_media),
        }
