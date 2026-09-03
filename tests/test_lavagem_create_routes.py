import uuid

import pytest

from app import create_app
from app.extensions import db
from app.models import (
    Cliente,
    Marca,
    Modelo,
    PorteVeiculo,
    Veiculo,
    OrdemServico,
    Lavagem,
)


@pytest.fixture
def client():
    app = create_app()
    return app.test_client()


@pytest.fixture
def ordem_servico_existente(app_context):
    identificador = uuid.uuid4().hex[:8]

    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=f"Cliente Create Lavagem {identificador}",
        email=f"create.lavagem.{identificador}@exemplo.com",
        telefone="48980000001",
    )

    marca = Marca(
        nome=f"Marca Create Lavagem {identificador}",
    )

    porte = PorteVeiculo(
        nome=f"Porte Create Lavagem {identificador}",
        ordem=91,
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
        nome=f"Modelo Create Lavagem {identificador}",
    )

    db.session.add(modelo)
    db.session.flush()

    veiculo = Veiculo(
        cliente_id=cliente.id,
        modelo_id=modelo.id,
        porte_id=porte.id,
        placa=f"C{identificador[:6]}",
        cor="Preto",
    )

    db.session.add(veiculo)
    db.session.flush()

    ordem_servico = OrdemServico(
        numero=f"OS-CR-{identificador}",
        cliente_id=cliente.id,
        veiculo_id=veiculo.id,
        valor_total=150,
        desconto=0,
        status="ABERTA",
    )

    db.session.add(ordem_servico)
    db.session.commit()

    ordem_servico_id = ordem_servico.id
    cliente_id = cliente.id
    marca_id = marca.id
    modelo_id = modelo.id
    porte_id = porte.id
    veiculo_id = veiculo.id

    yield ordem_servico_id

    db.session.rollback()

    lavagens = Lavagem.query.filter_by(
        ordem_servico_id=ordem_servico_id
    ).all()

    for lavagem in lavagens:
        db.session.delete(lavagem)

    db.session.flush()

    ordem_servico = db.session.get(
        OrdemServico,
        ordem_servico_id,
    )

    if ordem_servico is not None:
        db.session.delete(ordem_servico)

    veiculo = db.session.get(
        Veiculo,
        veiculo_id,
    )

    if veiculo is not None:
        db.session.delete(veiculo)

    modelo = db.session.get(
        Modelo,
        modelo_id,
    )

    if modelo is not None:
        db.session.delete(modelo)

    porte = db.session.get(
        PorteVeiculo,
        porte_id,
    )

    if porte is not None:
        db.session.delete(porte)

    marca = db.session.get(
        Marca,
        marca_id,
    )

    if marca is not None:
        db.session.delete(marca)

    cliente = db.session.get(
        Cliente,
        cliente_id,
    )

    if cliente is not None:
        db.session.delete(cliente)

    db.session.commit()


def test_criar_lavagem(
    client,
    ordem_servico_existente,
):
    response = client.post(
        "/lavagens",
        json={
            "ordem_servico_id": ordem_servico_existente,
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["id"] is not None
    assert data["ordem_servico_id"] == ordem_servico_existente
    assert data["status"] == "AGUARDANDO"
    assert data["inicio"] is None
    assert data["fim"] is None
    assert data["observacoes"] is None
    assert data["criado_em"] is not None
    assert data["atualizado_em"] is not None


def test_criar_lavagem_sem_ordem_servico(client):
    response = client.post(
        "/lavagens",
        json={},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["erro"] == "ordem_servico_id é obrigatório."


def test_criar_lavagem_com_ordem_servico_inexistente(client):
    response = client.post(
        "/lavagens",
        json={
            "ordem_servico_id": 999999,
        },
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["erro"] == "Ordem de Serviço não encontrada."