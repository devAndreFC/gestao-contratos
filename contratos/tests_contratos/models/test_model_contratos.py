# tests/test_contrato_model.py
from django.test import TestCase
from contratos.models import Contrato
from contratos.tests_contratos.factories import ContratoFactory
from decimal import Decimal


class ContratoModelTest(TestCase):
    def test_criacao_contrato(self):
        contrato = ContratoFactory()
        self.assertIsInstance(contrato, Contrato)
        self.assertTrue(contrato.pk)

    def test_str_method(self):
        contrato = ContratoFactory()
        self.assertEqual(
            str(contrato), f"Contrato {contrato.id} - {contrato.cpf}"
        )

    def test_campos_obrigatorios(self):
        contrato = ContratoFactory.build()
        self.assertIsNotNone(contrato.data_emissao)
        self.assertIsNotNone(contrato.data_nascimento_tomador)
        self.assertIsNotNone(contrato.valor_desembolsado)
        self.assertIsNotNone(contrato.cpf)
        self.assertIsNotNone(contrato.pais)
        self.assertIsNotNone(contrato.estado)
        self.assertIsNotNone(contrato.cidade)
        self.assertIsNotNone(contrato.numero_telefone)
        self.assertIsNotNone(contrato.taxa_contrato)

    def test_valor_desembolsado_decimal(self):
        contrato = ContratoFactory(valor_desembolsado=Decimal("1234.56"))
        self.assertEqual(contrato.valor_desembolsado, Decimal("1234.56"))
