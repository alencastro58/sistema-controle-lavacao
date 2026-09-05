import uuid
from datetime import datetime
from unittest.mock import patch

import pytest

from app.extensions import db
from app.models import (
    Marca,
    Modelo,
    PorteVeiculo,
    Servico,
    PrecoServico,
)


@pytest.fixture
def preco_servico_dados(app_context):
    sufixo = uuid.uuid4().hex[:8]

    marca = Marca(
        nome=f"Marca Route Preco {sufixo}",
    )

    porte = PorteVeiculo(
        nome=f"Porte Route Preco {sufixo}",
        ordem=97,
    )

    servico = Servico(
        nome=f"Servico Route Preco {sufixo}",
        descricao="Servico para teste de rotas de preco",
        valor=0,
        ativo=True,
    )

    db.session.add_all(
        [
            marca,
            porte,
            servico,
        ]
    )
    db.session.flush()

    modelo = Modelo(
        marca_id=marca.id,
        nome=f"Modelo Route Preco {sufixo}",
    )

    db.session.add(modelo)
    db.session.flush()

    preco = PrecoServico(
        servico_id=servico.id,
        porte_id=porte.id,
        valor=75.00,
        ativo=True,
    )

    db.session.add(preco)
    db.session.commit()

    dados = {
        "marca_id": marca.id,
        "modelo_id": modelo.id,
        "porte_id": porte.id,
        "servico_id": servico.id,
        "preco_id": preco.id,
        "sufixo": sufixo,
    }

    yield dados

    db.session.rollback()

    preco = db.session.get(
        PrecoServico,
        dados["preco_id"],
    )

    if preco is not None:
        db.session.delete(preco)

    servico = db.session.get(
        Servico,
        dados["servico_id"],
    )

    if servico is not None:
        db.session.delete(servico)

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

    db.session.commit()


@pytest.fixture
def dados_para_criacao_preco(app_context):
    sufixo = uuid.uuid4().hex[:8]

    marca = Marca(
        nome=f"Marca Criacao Preco {sufixo}",
    )

    porte = PorteVeiculo(
        nome=f"Porte Criacao Preco {sufixo}",
        ordem=98,
    )

    servico = Servico(
        nome=f"Servico Criacao Preco {sufixo}",
        descricao="Servico para teste de criacao de preco",
        valor=0,
        ativo=True,
    )

    db.session.add_all(
        [
            marca,
            porte,
            servico,
        ]
    )
    db.session.flush()

    dados = {
        "marca_id": marca.id,
        "porte_id": porte.id,
        "servico_id": servico.id,
    }

    db.session.commit()

    yield dados

    db.session.rollback()

    servico = db.session.get(
        Servico,
        dados["servico_id"],
    )

    if servico is not None:
        db.session.delete(servico)

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

    db.session.commit()


def test_criar_preco_servico(
    client,
    dados_para_criacao_preco,
):
    payload = {
        "servico_id": dados_para_criacao_preco["servico_id"],
        "porte_id": dados_para_criacao_preco["porte_id"],
        "valor": 85.00,
        "ativo": True,
    }

    response = client.post(
        "/precos-servicos",
        json=payload,
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["servico_id"] == dados_para_criacao_preco["servico_id"]
    assert data["porte_id"] == dados_para_criacao_preco["porte_id"]
    assert data["valor"] == 85.0
    assert data["ativo"] is True
    assert "id" in data
    assert "criado_em" in data
    assert "atualizado_em" in data

    preco = db.session.get(
        PrecoServico,
        data["id"],
    )

    if preco is not None:
        db.session.delete(preco)

    db.session.commit()


def test_criar_preco_servico_delega_para_service(
    client,
    preco_servico_dados,
):
    preco_servico = PrecoServico(
        id=999999,
        servico_id=preco_servico_dados["servico_id"],
        porte_id=preco_servico_dados["porte_id"],
        valor=95.00,
        ativo=True,
        criado_em=datetime.now(),
        atualizado_em=datetime.now(),
    )

    payload = {
        "servico_id": preco_servico_dados["servico_id"],
        "porte_id": preco_servico_dados["porte_id"],
        "valor": 95.00,
    }

    with patch(
        "app.routes.preco_servico.PrecoServicoService.criar",
        return_value=preco_servico,
    ) as mock_criar:
        response = client.post(
            "/precos-servicos",
            json=payload,
        )

    assert response.status_code == 201

    mock_criar.assert_called_once_with(payload)

    data = response.get_json()

    assert data["id"] == 999999
    assert data["servico_id"] == preco_servico_dados["servico_id"]
    assert data["porte_id"] == preco_servico_dados["porte_id"]
    assert data["valor"] == 95.0
    assert data["ativo"] is True


def test_criar_preco_servico_servico_obrigatorio(
    client,
    preco_servico_dados,
):
    payload = {
        "porte_id": preco_servico_dados["porte_id"],
        "valor": 50.00,
    }

    response = client.post(
        "/precos-servicos",
        json=payload,
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["erro"] == "servico_id é obrigatório."


def test_criar_preco_servico_porte_obrigatorio(
    client,
    preco_servico_dados,
):
    payload = {
        "servico_id": preco_servico_dados["servico_id"],
        "valor": 50.00,
    }

    response = client.post(
        "/precos-servicos",
        json=payload,
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["erro"] == "porte_id é obrigatório."


def test_criar_preco_servico_valor_obrigatorio(
    client,
    preco_servico_dados,
):
    payload = {
        "servico_id": preco_servico_dados["servico_id"],
        "porte_id": preco_servico_dados["porte_id"],
    }

    response = client.post(
        "/precos-servicos",
        json=payload,
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["erro"] == "valor é obrigatório."


def test_criar_preco_servico_metodo_nao_permitido(
    client,
):
    response = client.put(
        "/precos-servicos",
    )

    assert response.status_code == 405


def test_buscar_preco_servico(
    client,
    preco_servico_dados,
):
    response = client.get(
        f"/precos-servicos/{preco_servico_dados['preco_id']}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == preco_servico_dados["preco_id"]
    assert data["servico_id"] == preco_servico_dados["servico_id"]
    assert data["porte_id"] == preco_servico_dados["porte_id"]
    assert data["valor"] == 75.0
    assert data["ativo"] is True


def test_buscar_preco_servico_inexistente(
    client,
):
    response = client.get(
        "/precos-servicos/999999"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["erro"] == "Preço de Serviço não encontrado."


def test_buscar_preco_servico_metodo_nao_permitido(
    client,
):
    response = client.post(
        "/precos-servicos/999999",
    )

    assert response.status_code == 405


def test_listar_precos_servicos(
    client,
    preco_servico_dados,
):
    response = client.get(
        "/precos-servicos"
    )

    assert response.status_code == 200

    data = response.get_json()

    ids = [item["id"] for item in data]

    assert preco_servico_dados["preco_id"] in ids


def test_listar_precos_servicos_delega_para_service(
    client,
):
    precos_servicos = [
        PrecoServico(
            id=1,
            servico_id=10,
            porte_id=20,
            valor=40.00,
            ativo=True,
            criado_em=datetime.now(),
            atualizado_em=datetime.now(),
        ),
        PrecoServico(
            id=2,
            servico_id=10,
            porte_id=21,
            valor=50.00,
            ativo=True,
            criado_em=datetime.now(),
            atualizado_em=datetime.now(),
        ),
    ]

    with patch(
        "app.routes.preco_servico.PrecoServicoService.listar_todos",
        return_value=precos_servicos,
    ) as mock_listar:
        response = client.get(
            "/precos-servicos"
        )

    assert response.status_code == 200

    mock_listar.assert_called_once_with()

    data = response.get_json()

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["valor"] == 40.0
    assert data[1]["id"] == 2
    assert data[1]["valor"] == 50.0


def test_listar_precos_servicos_metodo_nao_permitido(
    client,
):
    response = client.put(
        "/precos-servicos",
    )

    assert response.status_code == 405


def test_excluir_preco_servico(
    client,
    preco_servico_dados,
):
    preco_id = preco_servico_dados["preco_id"]

    response = client.delete(
        f"/precos-servicos/{preco_id}"
    )

    assert response.status_code == 204

    resultado = db.session.get(
        PrecoServico,
        preco_id,
    )

    assert resultado is None


def test_excluir_preco_servico_inexistente(
    client,
):
    response = client.delete(
        "/precos-servicos/999999"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["erro"] == "Preço de Serviço não encontrado."


def test_excluir_preco_servico_metodo_nao_permitido(
    client,
):
    response = client.post(
        "/precos-servicos/999999",
    )

    assert response.status_code == 405
