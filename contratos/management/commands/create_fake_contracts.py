import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from contratos.models import Contrato, Parcela

User = get_user_model()


def gerar_cpf():
    return "".join(str(random.randint(0, 9)) for _ in range(11))


def gerar_telefone():
    prefixo = "+55 11 9"
    parte1 = random.randint(1000, 9999)
    parte2 = random.randint(1000, 9999)
    return f"{prefixo}{parte1}-{parte2}"


class Command(BaseCommand):
    help = "Cria 20 contratos fictícios com 10 parcelas cada"

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        if not user:
            self.stdout.write(
                self.style.ERROR(
                    "Nenhum usuário encontrado para atribuir como created_by"
                )
            )
            return

        for i in range(1, 21):
            data_emissao = date.today() - timedelta(days=random.randint(0, 365))
            data_nasc = date.today() - timedelta(
                days=random.randint(18 * 365, 70 * 365)
            )
            valor_desembolsado = round(random.uniform(1000, 10000), 2)
            taxa = round(random.uniform(1.0, 10.0), 2)

            contrato = Contrato.objects.create(
                data_emissao=data_emissao,
                data_nascimento_tomador=data_nasc,
                valor_desembolsado=valor_desembolsado,
                cpf=gerar_cpf(),
                pais="Brasil",
                estado=random.choice(["SP", "RJ", "MG", "RS", "BA"]),
                cidade=random.choice(
                    [
                        "São Paulo",
                        "Rio de Janeiro",
                        "Belo Horizonte",
                        "Porto Alegre",
                        "Salvador",
                        "Amazonnas",
                    ]
                ),
                numero_telefone=gerar_telefone(),
                taxa_contrato=taxa,
                created_by=user,
            )
            self.stdout.write(self.style.SUCCESS(f"Contrato {contrato.id} criado"))

            valor_parcela = round(valor_desembolsado / 10, 2)
            for parcela_num in range(1, 11):
                data_vencimento = data_emissao + timedelta(days=30 * parcela_num)
                Parcela.objects.create(
                    contrato=contrato,
                    numero_parcela=parcela_num,
                    valor_parcela=valor_parcela,
                    data_vencimento=data_vencimento,
                    created_by=user,
                )
            self.stdout.write(
                self.style.SUCCESS(f"10 parcelas criadas para contrato {contrato.id}")
            )

        self.stdout.write(self.style.SUCCESS("Script finalizado com sucesso!"))
