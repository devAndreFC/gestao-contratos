from django.test import TestCase
from contratos.models import Parcela
from contratos.tests_contratos.factories import ParcelaFactory


class ParcelaModelTest(TestCase):
    def test_criacao_parcela(self):
        parcela = ParcelaFactory()
        self.assertIsInstance(parcela, Parcela)
        self.assertTrue(parcela.pk)

    def test_str_method(self):
        parcela = ParcelaFactory(numero_parcela=3)
        expected_str = f"Parcela {parcela.numero_parcela} - Contrato {parcela.contrato.id}"
        self.assertEqual(str(parcela), expected_str)

    def test_campos_obrigatorios(self):
        parcela = ParcelaFactory.build()
        self.assertIsNotNone(parcela.contrato)
        self.assertIsNotNone(parcela.numero_parcela)
        self.assertIsNotNone(parcela.valor_parcela)
        self.assertIsNotNone(parcela.data_vencimento)
