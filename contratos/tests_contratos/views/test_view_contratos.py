from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from contratos.models import Contrato
from contratos.tests_contratos.factories import (
    ContratoFactory,
    ParcelaFactory,
    UserFactory,
)
from datetime import date


class ContratoViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse("contrato-list")

    def test_criar_contrato_sem_parcelas(self):
        data = {
            "data_emissao": "2024-01-01",
            "data_nascimento_tomador": "1990-01-01",
            "valor_desembolsado": "1000.00",
            "cpf": "12345678901",
            "pais": "Brasil",
            "estado": "SP",
            "cidade": "São Paulo",
            "numero_telefone": "11999999999",
            "taxa_contrato": "1.23",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contrato = Contrato.objects.get(id=response.data["id"])
        self.assertEqual(contrato.created_by, self.user)
        self.assertEqual(contrato.parcelas.count(), 0)

    def test_criar_contrato_com_parcelas(self):
        data = {
            "data_emissao": "2024-01-01",
            "data_nascimento_tomador": "1990-01-01",
            "valor_desembolsado": "1000.00",
            "cpf": "12345678901",
            "pais": "Brasil",
            "estado": "SP",
            "cidade": "São Paulo",
            "numero_telefone": "11999999999",
            "taxa_contrato": "1.23",
            "parcelas": [
                {
                    "numero_parcela": 1,
                    "valor_parcela": "500.00",
                    "data_vencimento": "2024-07-01",
                },
                {
                    "numero_parcela": 2,
                    "valor_parcela": "500.00",
                    "data_vencimento": "2024-08-01",
                },
            ],
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contrato = Contrato.objects.get(id=response.data["id"])
        self.assertEqual(contrato.parcelas.count(), 2)

    def test_listagem_contratos(self):
        contrato = ContratoFactory(created_by=self.user)
        ParcelaFactory(contrato=contrato, created_by=self.user)

        url = reverse("contrato-list")
        response = self.client.get(url)

        self.assertIn("results", response.data)
        self.assertIsInstance(response.data["results"], list)
        self.assertTrue(response.data["results"])

        contrato_data = response.data["results"][0]
        self.assertIn("total_parcelas", contrato_data)
        self.assertEqual(contrato_data["total_parcelas"], 1)

    def test_atualizar_contrato_somente_dados(self):
        contrato = ContratoFactory(created_by=self.user)
        ParcelaFactory(contrato=contrato, created_by=self.user)

        url = reverse("contrato-detail", args=[contrato.id])
        data = {
            "data_emissao": "2024-06-01",
            "data_nascimento_tomador": "1991-01-01",
            "valor_desembolsado": "2000.00",
            "cpf": "98765432100",
            "pais": "Brasil",
            "estado": "RJ",
            "cidade": "Rio de Janeiro",
            "numero_telefone": "21999999999",
            "taxa_contrato": "2.50",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contrato.refresh_from_db()
        self.assertEqual(contrato.cidade, "Rio de Janeiro")
        self.assertGreaterEqual(contrato.parcelas.count(), 1)

    def test_endpoint_resumo(self):
        contrato1 = ContratoFactory(
            created_by=self.user, valor_desembolsado=1000.00, taxa_contrato=2.0
        )
        ParcelaFactory(contrato=contrato1, valor_parcela=500.00, created_by=self.user)
        ParcelaFactory(contrato=contrato1, valor_parcela=500.00, created_by=self.user)

        contrato2 = ContratoFactory(
            created_by=self.user, valor_desembolsado=2000.00, taxa_contrato=3.0
        )
        ParcelaFactory(contrato=contrato2, valor_parcela=1000.00, created_by=self.user)

        url = reverse("contrato-resumo")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["valor_total_a_receber"], 2000.00)
        self.assertEqual(response.data["valor_total_desembolsado"], 3000.00)
        self.assertEqual(response.data["numero_total_contratos"], 2)
        self.assertEqual(response.data["taxa_media"], 2.5)


class ContratoViewSetFiltroTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.contrato1 = ContratoFactory(
            created_by=self.user,
            data_emissao=date(2024, 5, 1),
            cpf="12345678900",
            estado="SP",
        )
        self.contrato2 = ContratoFactory(
            created_by=self.user,
            data_emissao=date(2023, 5, 1),
            cpf="98765432100",
            estado="RJ",
        )

    def test_filtrar_por_id(self):
        url = reverse("contrato-list")
        response = self.client.get(url, {"id": self.contrato1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["id"], self.contrato1.id)

    def test_filtrar_por_cpf(self):
        url = reverse("contrato-list")
        response = self.client.get(url, {"cpf": self.contrato2.cpf})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["cpf"],
            self.contrato2.cpf,
        )

    def test_filtrar_por_estado(self):
        url = reverse("contrato-list")
        response = self.client.get(url, {"estado": "sp"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.contrato1.id)

    def test_filtrar_por_data_mes_ano(self):
        url = reverse("contrato-list")
        response = self.client.get(url, {"data": "05/2024"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["id"], self.contrato1.id)

    def test_filtrar_por_data_ano(self):
        url = reverse("contrato-list")
        response = self.client.get(url, {"data": "2023"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["id"], self.contrato2.id)

    def test_filtrar_por_data_formato_invalido(self):
        url = reverse("contrato-list")
        response = self.client.get(url, {"data": "invalido"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
