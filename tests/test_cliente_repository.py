import uuid

import pytest

from app.extensions import db
from app.models.cliente import Cliente
from app.repositories.cliente_repository import ClienteRepository


@pytest.fixture
def cliente_dados(app_context):
    sufixo = uuid.uuid4().hex[:8]

    cliente_1 = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=f"Cliente Repository 1 {sufixo}",
        cpf_cnpj=f"123456789{sufixo[:5]}",
        email=f"cliente1_{sufixo}@teste.com",
        telefone="48999990001",
        ativo=True,
    )

    cliente_2 = Cliente(
        tipo_pessoa="PJ",
        nome_razao_social=f"Cliente Repository 2 {sufixo}",
        cpf_cnpj=f"987654321{sufixo[:5]}",
        email=f"cliente2_{sufixo}@teste.com",
        telefone="48999990002",
        ativo=False,
    )

    db.session.add_all(
        [
            cliente_1,
            cliente_2,
        ]
    )
    db.session.commit()

    dados = {
        "cliente_1_id": cliente_1.id,
        "cliente_2_id": cliente_2.id,
        "cliente_1_cpf_cnpj": cliente_1.cpf_cnpj,
        "cliente_2_cpf_cnpj": cliente_2.cpf_cnpj,
    }

    yield dados

    db.session.rollback()

    for cliente_id in [
        dados["cliente_1_id"],
        dados["cliente_2_id"],
    ]:
        cliente = db.session.get(
            Cliente,
            cliente_id,
        )

        if cliente is not None:
            db.session.delete(cliente)

    db.session.commit()


@pytest.mark.usefixtures("app_context")
def test_salvar_cliente():
    sufixo = uuid.uuid4().hex[:8]

    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=f"Cliente Salvar {sufixo}",
        email=f"salvar_{sufixo}@teste.com",
        telefone="48999990003",
        ativo=True,
    )

    resultado = ClienteRepository.salvar(cliente)
    db.session.commit()

    assert resultado is cliente
    assert resultado.id is not None

    db.session.delete(cliente)
    db.session.commit()


@pytest.mark.usefixtures("app_context")
def test_buscar_cliente_por_id(cliente_dados):
    resultado = ClienteRepository.buscar_por_id(
        cliente_dados["cliente_1_id"]
    )

    assert resultado is not None
    assert resultado.id == cliente_dados["cliente_1_id"]


@pytest.mark.usefixtures("app_context")
def test_buscar_cliente_por_id_retorna_none_quando_nao_encontrado():
    resultado = ClienteRepository.buscar_por_id(999999)

    assert resultado is None


@pytest.mark.usefixtures("app_context")
def test_buscar_cliente_por_cpf_cnpj(cliente_dados):
    resultado = ClienteRepository.buscar_por_cpf_cnpj(
        cliente_dados["cliente_1_cpf_cnpj"]
    )

    assert resultado is not None
    assert resultado.id == cliente_dados["cliente_1_id"]


@pytest.mark.usefixtures("app_context")
def test_buscar_cliente_por_cpf_cnpj_retorna_none_quando_nao_encontrado():
    resultado = ClienteRepository.buscar_por_cpf_cnpj(
        "00000000000000"
    )

    assert resultado is None


@pytest.mark.usefixtures("app_context")
def test_listar_todos_clientes(cliente_dados):
    lista = ClienteRepository.listar_todos()

    ids = {cliente.id for cliente in lista}

    assert cliente_dados["cliente_1_id"] in ids
    assert cliente_dados["cliente_2_id"] in ids


@pytest.mark.usefixtures("app_context")
def test_listar_clientes_ativos(cliente_dados):
    lista = ClienteRepository.listar_ativos()

    ids = {cliente.id for cliente in lista}

    assert cliente_dados["cliente_1_id"] in ids
    assert cliente_dados["cliente_2_id"] not in ids


@pytest.mark.usefixtures("app_context")
def test_excluir_cliente(cliente_dados):
    cliente = ClienteRepository.buscar_por_id(
        cliente_dados["cliente_1_id"]
    )

    assert cliente is not None

    ClienteRepository.excluir(cliente)
    db.session.commit()

    resultado = ClienteRepository.buscar_por_id(
        cliente_dados["cliente_1_id"]
    )

    assert resultado is None