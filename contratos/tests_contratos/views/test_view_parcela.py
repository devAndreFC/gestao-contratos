from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from contratos.tests_contratos.factories import (
    ParcelaFactory,
    ContratoFactory,
    UserFactory,
)


class ParcelaViewSetTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.contrato = ContratoFactory(created_by=self.user)
        self.parcela = ParcelaFactory(contrato=self.contrato, created_by=self.user)

    def test_listar_parcelas(self):
        url = reverse("parcela-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertTrue(len(response.data["results"]) > 0)

    def test_criar_parcela(self):
        url = reverse("parcela-list")
        data = {
            "contrato": self.contrato.id,
            "numero_parcela": 2,
            "valor_parcela": "1500.50",
            "data_vencimento": "2025-07-15",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["numero_parcela"], 2)
        self.assertEqual(response.data["created_by"], self.user.id)
        self.assertEqual(response.data["updated_by"], self.user.id)

    def test_atualizar_parcela(self):
        url = reverse("parcela-detail", args=[self.parcela.id])
        data = {
            "numero_parcela": 10,
            "valor_parcela": "999.99",
            "data_vencimento": "2025-08-01",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.parcela.refresh_from_db()
        self.assertEqual(self.parcela.numero_parcela, 10)
        self.assertEqual(str(self.parcela.valor_parcela), "999.99")
