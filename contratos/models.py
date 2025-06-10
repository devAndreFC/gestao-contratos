from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.DO_NOTHING,
        related_name="%(class)s_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated",
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Contrato(BaseModel):
    data_emissao = models.DateField()
    data_nascimento_tomador = models.DateField()
    valor_desembolsado = models.DecimalField(max_digits=12, decimal_places=2)
    cpf = models.CharField(max_length=14)
    pais = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    numero_telefone = models.CharField(max_length=20)
    taxa_contrato = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Contrato {self.id} - {self.cpf}"


class Parcela(BaseModel):
    contrato = models.ForeignKey(
        Contrato, related_name="parcelas", on_delete=models.CASCADE
    )
    numero_parcela = models.PositiveIntegerField()
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()

    def __str__(self):
        return f"Parcela {self.numero_parcela} - Contrato {self.contrato.id}"
