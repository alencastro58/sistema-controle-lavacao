import uuid

import pytest

from app.extensions import db
from app.models import (
    Cliente,
    Marca,
    Modelo,
    PorteVeiculo,
    Veiculo,
    OrdemServico,
)
from app.repositories.ordem_servico_repository import OrdemServicoRepository


@pytest.fixture
def ordem_servico_dados(app_context):
    identificador = uuid.uuid4().hex[:8]

    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=f"Cliente Repo OS {identificador}",
        email=f"repo.os.{identificador}@exemplo.com",
        telefone="48980000004",
    )

    marca = Marca(
        nome=f"Marca Repo OS {identificador}",
    )

    porte = PorteVeiculo(
        nome=f"Porte Repo OS {identificador}",
        ordem=90,
    )

    db.session.add_all(
        [
            cliente,
            marca,
            porte,
        ]
    )
    db.session.flush()

    modelo = Modelo(
        marca_id=marca.id,
        nome=f"Modelo Repo OS {identificador}",
    )

    db.session.add(modelo)
    db.session.flush()

    veiculo = Veiculo(
        cliente_id=cliente.id,
        modelo_id=modelo.id,
        porte_id=porte.id,
        placa=f"R{identificador[:6]}",
        cor="Preto",
    )

    db.session.add(veiculo)
    db.session.flush()

    ordem_1 = OrdemServico(
        numero=f"OS-REPO-{identificador}",
        cliente_id=cliente.id,
        veiculo_id=veiculo.id,
        valor_total=100,
        desconto=0,
        status="ABERTA",
    )

    identificador_2 = uuid.uuid4().hex[:8]

    ordem_2 = OrdemServico(
        numero=f"OS-REPO-{identificador_2}",
        cliente_id=cliente.id,
        veiculo_id=veiculo.id,
        valor_total=200,
        desconto=10,
        status="ABERTA",
    )

    db.session.add_all(
        [
            ordem_1,
            ordem_2,
        ]
    )
    db.session.flush()

    dados = {
        "cliente_id": cliente.id,
        "marca_id": marca.id,
        "modelo_id": modelo.id,
        "porte_id": porte.id,
        "veiculo_id": veiculo.id,
        "ordem_1_id": ordem_1.id,
        "ordem_2_id": ordem_2.id,
    }

    db.session.commit()

    yield dados

    db.session.rollback()

    for ordem_id in [
        dados["ordem_1_id"],
        dados["ordem_2_id"],
    ]:
        ordem = db.session.get(
            OrdemServico,
            ordem_id,
        )

        if ordem is not None:
            db.session.delete(ordem)

    db.session.flush()

    veiculo = db.session.get(
        Veiculo,
        dados["veiculo_id"],
    )

    if veiculo is not None:
        db.session.delete(veiculo)

    modelo = db.session.get(
        Modelo,
        dados["modelo_id"],
    )

    if modelo is not None:
        db.session.delete(modelo)

    porte = db.session.get(
        PorteVeiculo,
        dados["porte_id"],
    )

    if porte is not None:
        db.session.delete(porte)

    marca = db.session.get(
        Marca,
        dados["marca_id"],
    )

    if marca is not None:
        db.session.delete(marca)

    cliente = db.session.get(
        Cliente,
        dados["cliente_id"],
    )

    if cliente is not None:
        db.session.delete(cliente)

    db.session.commit()


def test_salvar_retorna_ordem_servico(
    app_context,
    ordem_servico_dados,
):
    ordem = db.session.get(
        OrdemServico,
        ordem_servico_dados["ordem_1_id"],
    )

    resultado = OrdemServicoRepository.salvar(ordem)

    assert resultado is ordem


def test_buscar_por_id_retorna_ordem_servico(
    app_context,
    ordem_servico_dados,
):
    ordem = OrdemServicoRepository.buscar_por_id(
        ordem_servico_dados["ordem_1_id"]
    )

    assert ordem is not None
    assert ordem.id == ordem_servico_dados["ordem_1_id"]


def test_buscar_por_id_retorna_none_quando_nao_encontrada(
    app_context,
):
    resultado = OrdemServicoRepository.buscar_por_id(999999)

    assert resultado is None


def test_listar_todas_retorna_ordens(
    app_context,
    ordem_servico_dados,
):
    ordens = OrdemServicoRepository.listar_todas()

    ids = [ordem.id for ordem in ordens]

    assert ordem_servico_dados["ordem_1_id"] in ids
    assert ordem_servico_dados["ordem_2_id"] in ids


def test_listar_por_cliente_retorna_ordens_do_cliente(
    app_context,
    ordem_servico_dados,
):
    ordens = OrdemServicoRepository.listar_por_cliente(
        ordem_servico_dados["cliente_id"]
    )

    ids = [ordem.id for ordem in ordens]

    assert ordem_servico_dados["ordem_1_id"] in ids
    assert ordem_servico_dados["ordem_2_id"] in ids


def test_listar_por_veiculo_retorna_ordens_do_veiculo(
    app_context,
    ordem_servico_dados,
):
    ordens = OrdemServicoRepository.listar_por_veiculo(
        ordem_servico_dados["veiculo_id"]
    )

    ids = [ordem.id for ordem in ordens]

    assert ordem_servico_dados["ordem_1_id"] in ids
    assert ordem_servico_dados["ordem_2_id"] in ids


def test_excluir_remove_ordem_servico(
    app_context,
    ordem_servico_dados,
):
    ordem = OrdemServicoRepository.buscar_por_id(
        ordem_servico_dados["ordem_1_id"]
    )

    assert ordem is not None

    OrdemServicoRepository.excluir(ordem)
    db.session.commit()

    resultado = OrdemServicoRepository.buscar_por_id(
        ordem_servico_dados["ordem_1_id"]
    )

    assert resultado is None
