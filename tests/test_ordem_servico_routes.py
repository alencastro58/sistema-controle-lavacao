import uuid
from datetime import datetime
from unittest.mock import patch

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


@pytest.fixture
def ordem_servico_dados(app_context):
    identificador = uuid.uuid4().hex[:8]

    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=f"Cliente POST OS {identificador}",
        email=f"post.os.{identificador}@exemplo.com",
        telefone="48980000006",
    )

    marca = Marca(
        nome=f"Marca POST OS {identificador}",
    )

    porte = PorteVeiculo(
        nome=f"Porte POST OS {identificador}",
        ordem=92,
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
        nome=f"Modelo POST OS {identificador}",
    )

    db.session.add(modelo)
    db.session.flush()

    veiculo = Veiculo(
        cliente_id=cliente.id,
        modelo_id=modelo.id,
        porte_id=porte.id,
        placa=f"P{identificador[:6]}",
        cor="Preto",
    )

    db.session.add(veiculo)
    db.session.flush()

    db.session.commit()

    dados = {
        "cliente_id": cliente.id,
        "marca_id": marca.id,
        "modelo_id": modelo.id,
        "porte_id": porte.id,
        "veiculo_id": veiculo.id,
        "identificador": identificador,
    }

    yield dados

    db.session.rollback()

    ordens_servico = (
        db.session.query(OrdemServico)
        .filter(
            OrdemServico.cliente_id == dados["cliente_id"]
        )
        .all()
    )

    for ordem_servico in ordens_servico:
        db.session.delete(ordem_servico)

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


def test_criar_ordem_servico(
    client,
    ordem_servico_dados,
):
    numero = (
        f"OS-POST-{ordem_servico_dados['identificador']}"
    )

    payload = {
        "numero": numero,
        "cliente_id": ordem_servico_dados["cliente_id"],
        "veiculo_id": ordem_servico_dados["veiculo_id"],
        "valor_total": 250,
        "desconto": 20,
        "status": "ABERTA",
        "observacoes": "Teste de criação via rota",
    }

    response = client.post(
        "/ordens-servico",
        json=payload,
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["numero"] == numero
    assert data["cliente_id"] == ordem_servico_dados["cliente_id"]
    assert data["veiculo_id"] == ordem_servico_dados["veiculo_id"]
    assert data["valor_total"] == 250.0
    assert data["desconto"] == 20.0
    assert data["status"] == "ABERTA"
    assert data["observacoes"] == "Teste de criação via rota"
    assert "id" in data
    assert "criado_em" in data
    assert "atualizado_em" in data


def test_criar_ordem_servico_delega_para_service(
    client,
    ordem_servico_dados,
):
    numero = (
        f"OS-SERVICE-{ordem_servico_dados['identificador']}"
    )

    ordem_servico = OrdemServico(
        id=999999,
        numero=numero,
        cliente_id=ordem_servico_dados["cliente_id"],
        veiculo_id=ordem_servico_dados["veiculo_id"],
        data_agendamento=None,
        valor_total=250,
        desconto=20,
        status="ABERTA",
        observacoes="Teste de delegação",
        criado_em=datetime.now(),
        atualizado_em=datetime.now(),
    )

    payload = {
        "numero": numero,
        "cliente_id": ordem_servico_dados["cliente_id"],
        "veiculo_id": ordem_servico_dados["veiculo_id"],
    }

    with patch(
        "app.routes.ordem_servico.OrdemServicoService.criar",
        return_value=ordem_servico,
    ) as mock_criar:
        response = client.post(
            "/ordens-servico",
            json=payload,
        )

    assert response.status_code == 201

    mock_criar.assert_called_once_with(payload)

    data = response.get_json()

    assert data["id"] == 999999
    assert data["numero"] == numero
    assert data["cliente_id"] == ordem_servico_dados["cliente_id"]
    assert data["veiculo_id"] == ordem_servico_dados["veiculo_id"]


def test_criar_ordem_servico_numero_obrigatorio(
    client,
    ordem_servico_dados,
):
    payload = {
        "cliente_id": ordem_servico_dados["cliente_id"],
        "veiculo_id": ordem_servico_dados["veiculo_id"],
    }

    response = client.post(
        "/ordens-servico",
        json=payload,
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["erro"] == "numero é obrigatório."


def test_criar_ordem_servico_cliente_obrigatorio(
    client,
    ordem_servico_dados,
):
    payload = {
        "numero": f"OS-POST-{ordem_servico_dados['identificador']}-002",
        "veiculo_id": ordem_servico_dados["veiculo_id"],
    }

    response = client.post(
        "/ordens-servico",
        json=payload,
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["erro"] == "cliente_id é obrigatório."


def test_criar_ordem_servico_veiculo_obrigatorio(
    client,
    ordem_servico_dados,
):
    payload = {
        "numero": f"OS-POST-{ordem_servico_dados['identificador']}-003",
        "cliente_id": ordem_servico_dados["cliente_id"],
    }

    response = client.post(
        "/ordens-servico",
        json=payload,
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["erro"] == "veiculo_id é obrigatório."


def test_criar_ordem_servico_metodo_nao_permitido(
    client,
):
    response = client.put(
        "/ordens-servico",
    )

    assert response.status_code == 405


def test_buscar_ordem_servico(
    client,
    ordem_servico_dados,
):
    numero = (
        f"OS-GET-{ordem_servico_dados['identificador']}"
    )

    ordem_servico = OrdemServico(
        numero=numero,
        cliente_id=ordem_servico_dados["cliente_id"],
        veiculo_id=ordem_servico_dados["veiculo_id"],
        valor_total=150,
        desconto=0,
        status="ABERTA",
        observacoes="OS de teste",
    )

    db.session.add(ordem_servico)
    db.session.commit()

    response = client.get(
        f"/ordens-servico/{ordem_servico.id}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == ordem_servico.id
    assert data["numero"] == numero
    assert data["cliente_id"] == ordem_servico_dados["cliente_id"]
    assert data["veiculo_id"] == ordem_servico_dados["veiculo_id"]


def test_buscar_ordem_servico_inexistente(
    client,
):
    response = client.get(
        "/ordens-servico/999999"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["erro"] == "Ordem de Serviço não encontrada."


def test_buscar_ordem_servico_metodo_nao_permitido(
    client,
):
    response = client.post(
        "/ordens-servico/999999",
    )

    assert response.status_code == 405

def test_listar_ordens_servico(
    client,
    ordem_servico_dados,
):
    numero_1 = (
        f"OS-L-{ordem_servico_dados['identificador']}-1"
    )
    numero_2 = (
        f"OS-L-{ordem_servico_dados['identificador']}-2"
    )

    ordem_1 = OrdemServico(
        numero=numero_1,
        cliente_id=ordem_servico_dados["cliente_id"],
        veiculo_id=ordem_servico_dados["veiculo_id"],
        valor_total=100,
        desconto=0,
        status="ABERTA",
    )

    ordem_2 = OrdemServico(
        numero=numero_2,
        cliente_id=ordem_servico_dados["cliente_id"],
        veiculo_id=ordem_servico_dados["veiculo_id"],
        valor_total=200,
        desconto=10,
        status="ABERTA",
    )

    db.session.add_all([ordem_1, ordem_2])
    db.session.commit()

    response = client.get(
        "/ordens-servico"
    )

    assert response.status_code == 200

    data = response.get_json()

    numeros = [item["numero"] for item in data]

    assert numero_1 in numeros
    assert numero_2 in numeros


def test_listar_ordens_servico_delega_para_service(
    client,
):
    ordens_servico = [
        OrdemServico(
            id=1,
            numero="OS-LISTA-SERVICE-001",
            cliente_id=10,
            veiculo_id=20,
            criado_em=datetime.now(),
            atualizado_em=datetime.now(),
        ),
        OrdemServico(
            id=2,
            numero="OS-LISTA-SERVICE-002",
            cliente_id=11,
            veiculo_id=21,
            criado_em=datetime.now(),
            atualizado_em=datetime.now(),
        ),
    ]

    with patch(
        "app.routes.ordem_servico.OrdemServicoService.listar_todas",
        return_value=ordens_servico,
    ) as mock_listar:
        response = client.get(
            "/ordens-servico"
        )

    assert response.status_code == 200

    mock_listar.assert_called_once_with()

    data = response.get_json()

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["numero"] == "OS-LISTA-SERVICE-001"
    assert data[1]["id"] == 2
    assert data[1]["numero"] == "OS-LISTA-SERVICE-002"


def test_listar_ordens_servico_metodo_nao_permitido(
    client,
):
    response = client.put(
        "/ordens-servico",
    )

    assert response.status_code == 405



