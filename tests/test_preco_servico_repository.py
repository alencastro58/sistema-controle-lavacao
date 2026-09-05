import uuid

import pytest

from app.extensions import db
from app.models import (
    Marca,
    Modelo,
    PorteVeiculo,
    Servico,
    PrecoServico,
)
from app.repositories.preco_servico_repository import PrecoServicoRepository


@pytest.fixture
def preco_servico_dados(app_context):
    sufixo = uuid.uuid4().hex[:8]

    marca = Marca(
        nome=f"Marca Preco {sufixo}",
    )

    porte_1 = PorteVeiculo(
        nome=f"Porte Preco 1 {sufixo}",
        ordem=95,
    )

    porte_2 = PorteVeiculo(
        nome=f"Porte Preco 2 {sufixo}",
        ordem=96,
    )

    servico_1 = Servico(
        nome=f"Servico Preco 1 {sufixo}",
        descricao="Servico para teste de precos",
        valor=0,
        ativo=True,
    )

    servico_2 = Servico(
        nome=f"Servico Preco 2 {sufixo}",
        descricao="Segundo servico para teste",
        valor=0,
        ativo=True,
    )

    db.session.add_all(
        [
            marca,
            porte_1,
            porte_2,
            servico_1,
            servico_2,
        ]
    )
    db.session.flush()

    modelo = Modelo(
        marca_id=marca.id,
        nome=f"Modelo Preco {sufixo}",
    )

    db.session.add(modelo)
    db.session.flush()

    preco_1 = PrecoServico(
        servico_id=servico_1.id,
        porte_id=porte_1.id,
        valor=40.00,
        ativo=True,
    )

    preco_2 = PrecoServico(
        servico_id=servico_1.id,
        porte_id=porte_2.id,
        valor=50.00,
        ativo=True,
    )

    preco_3 = PrecoServico(
        servico_id=servico_2.id,
        porte_id=porte_1.id,
        valor=60.00,
        ativo=True,
    )

    db.session.add_all(
        [
            preco_1,
            preco_2,
            preco_3,
        ]
    )
    db.session.flush()

    dados = {
        "marca_id": marca.id,
        "modelo_id": modelo.id,
        "porte_1_id": porte_1.id,
        "porte_2_id": porte_2.id,
        "servico_1_id": servico_1.id,
        "servico_2_id": servico_2.id,
        "preco_1_id": preco_1.id,
        "preco_2_id": preco_2.id,
        "preco_3_id": preco_3.id,
    }

    db.session.commit()

    yield dados

    db.session.rollback()

    for preco_id in [
        dados["preco_1_id"],
        dados["preco_2_id"],
        dados["preco_3_id"],
    ]:
        preco = db.session.get(
            PrecoServico,
            preco_id,
        )

        if preco is not None:
            db.session.delete(preco)

    db.session.flush()

    for servico_id in [
        dados["servico_1_id"],
        dados["servico_2_id"],
    ]:
        servico = db.session.get(
            Servico,
            servico_id,
        )

        if servico is not None:
            db.session.delete(servico)

    modelo = db.session.get(
        Modelo,
        dados["modelo_id"],
    )

    if modelo is not None:
        db.session.delete(modelo)

    for porte_id in [
        dados["porte_1_id"],
        dados["porte_2_id"],
    ]:
        porte = db.session.get(
            PorteVeiculo,
            porte_id,
        )

        if porte is not None:
            db.session.delete(porte)

    marca = db.session.get(
        Marca,
        dados["marca_id"],
    )

    if marca is not None:
        db.session.delete(marca)

    db.session.commit()


@pytest.mark.usefixtures("app_context")
def test_salvar_preco_servico(preco_servico_dados):
    preco = db.session.get(
        PrecoServico,
        preco_servico_dados["preco_1_id"],
    )

    resultado = PrecoServicoRepository.salvar(preco)

    assert resultado is preco


@pytest.mark.usefixtures("app_context")
def test_buscar_preco_servico_por_id(preco_servico_dados):
    resultado = PrecoServicoRepository.buscar_por_id(
        preco_servico_dados["preco_1_id"]
    )

    assert resultado is not None
    assert resultado.id == preco_servico_dados["preco_1_id"]


@pytest.mark.usefixtures("app_context")
def test_buscar_preco_servico_por_id_retorna_none_quando_nao_encontrado():
    resultado = PrecoServicoRepository.buscar_por_id(999999)

    assert resultado is None


@pytest.mark.usefixtures("app_context")
def test_listar_todos_precos_servicos(preco_servico_dados):
    lista = PrecoServicoRepository.listar_todos()

    ids = {preco.id for preco in lista}

    assert preco_servico_dados["preco_1_id"] in ids
    assert preco_servico_dados["preco_2_id"] in ids
    assert preco_servico_dados["preco_3_id"] in ids


@pytest.mark.usefixtures("app_context")
def test_listar_precos_por_servico(preco_servico_dados):
    lista = PrecoServicoRepository.listar_por_servico(
        preco_servico_dados["servico_1_id"]
    )

    assert len(lista) == 2

    assert {preco.id for preco in lista} == {
        preco_servico_dados["preco_1_id"],
        preco_servico_dados["preco_2_id"],
    }


@pytest.mark.usefixtures("app_context")
def test_listar_precos_por_porte(preco_servico_dados):
    lista = PrecoServicoRepository.listar_por_porte(
        preco_servico_dados["porte_1_id"]
    )

    assert len(lista) == 2

    assert {preco.id for preco in lista} == {
        preco_servico_dados["preco_1_id"],
        preco_servico_dados["preco_3_id"],
    }


@pytest.mark.usefixtures("app_context")
def test_excluir_preco_servico(preco_servico_dados):
    preco = PrecoServicoRepository.buscar_por_id(
        preco_servico_dados["preco_1_id"]
    )

    assert preco is not None

    PrecoServicoRepository.excluir(preco)
    db.session.commit()

    resultado = PrecoServicoRepository.buscar_por_id(
        preco_servico_dados["preco_1_id"]
    )

    assert resultado is None
