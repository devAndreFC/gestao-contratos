# tests/factories.py
import factory
from contratos.models import Contrato, Parcela
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "testpassword")
    is_active = True
    is_staff = False
    is_superuser = False


class ContratoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contrato

    data_emissao = factory.Faker("date_this_decade")
    data_nascimento_tomador = factory.Faker("date_of_birth")
    valor_desembolsado = factory.Faker(
        "pydecimal", left_digits=5, right_digits=2, positive=True
    )
    cpf = factory.Faker("numerify", text="###########")
    pais = "Brasil"
    estado = factory.Faker("state_abbr")
    cidade = factory.Faker("city")
    numero_telefone = numero_telefone = factory.Faker("phone_number", locale="pt_BR")
    taxa_contrato = factory.Faker(
        "pydecimal", left_digits=1, right_digits=2, positive=True
    )
    created_by = factory.SubFactory(UserFactory)

class ParcelaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parcela

    contrato = factory.SubFactory(ContratoFactory)
    numero_parcela = factory.Sequence(lambda n: n + 1)
    valor_parcela = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    data_vencimento = factory.Faker("future_date")
    created_by = factory.SubFactory(UserFactory)
