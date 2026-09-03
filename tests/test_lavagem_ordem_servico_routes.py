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
def ordem_servico_com_lavagens(app_context):
    identificador = uuid.uuid4().hex[:8]

    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=f"Cliente OS Lavagem {identificador}",
        email=f"os.lavagem.{identificador}@exemplo.com",
        telefone="48980000003",
    )

    marca = Marca(
        nome=f"Marca OS Lavagem {identificador}",
    )

    porte = PorteVeiculo(
        nome=f"Porte OS Lavagem {identificador}",
        ordem=89,
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
        nome=f"Modelo OS Lavagem {identificador}",
    )

    db.session.add(modelo)
    db.session.flush()

    veiculo = Veiculo(
        cliente_id=cliente.id,
        modelo_id=modelo.id,
        porte_id=porte.id,
        placa=f"O{identificador[:6]}",
        cor="Branco",
    )

    db.session.add(veiculo)
    db.session.flush()

    ordem_servico = OrdemServico(
        numero=f"OS-OR-LV-{identificador}",
        cliente_id=cliente.id,
        veiculo_id=veiculo.id,
        valor_total=250,
        desconto=0,
        status="ABERTA",
    )

    db.session.add(ordem_servico)
    db.session.flush()

    lavagem_1 = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status="AGUARDANDO",
        observacoes="Lavagem OS teste 1",
    )

    lavagem_2 = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status="AGUARDANDO",
        observacoes="Lavagem OS teste 2",
    )

    db.session.add_all(
        [
            lavagem_1,
            lavagem_2,
        ]
    )
    db.session.commit()

    dados = {
        "ordem_servico_id": ordem_servico.id,
        "lavagem_1_id": lavagem_1.id,
        "lavagem_2_id": lavagem_2.id,
        "veiculo_id": veiculo.id,
        "modelo_id": modelo.id,
        "porte_id": porte.id,
        "marca_id": marca.id,
        "cliente_id": cliente.id,
    }

    yield dados

    db.session.rollback()

    for lavagem_id in [
        lavagem_1.id,
        lavagem_2.id,
    ]:
        lavagem = db.session.get(
            Lavagem,
            lavagem_id,
        )

        if lavagem is not None:
            db.session.delete(lavagem)

    db.session.flush()

    ordem_servico = db.session.get(
        OrdemServico,
        dados["ordem_servico_id"],
    )

    if ordem_servico is not None:
        db.session.delete(ordem_servico)

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


def test_listar_lavagens_por_ordem_servico(
    client,
    ordem_servico_com_lavagens,
):
    ordem_servico_id = ordem_servico_com_lavagens["ordem_servico_id"]

    response = client.get(
        f"/ordens-servico/{ordem_servico_id}/lavagens"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 2

    ids = [lavagem["id"] for lavagem in data]

    assert ordem_servico_com_lavagens["lavagem_1_id"] in ids
    assert ordem_servico_com_lavagens["lavagem_2_id"] in ids


def test_listar_lavagens_por_ordem_servico_retorna_dados(
    client,
    ordem_servico_com_lavagens,
):
    ordem_servico_id = ordem_servico_com_lavagens["ordem_servico_id"]

    response = client.get(
        f"/ordens-servico/{ordem_servico_id}/lavagens"
    )

    assert response.status_code == 200

    data = response.get_json()

    lavagens = {
        lavagem["id"]: lavagem
        for lavagem in data
    }

    lavagem_1 = lavagens[
        ordem_servico_com_lavagens["lavagem_1_id"]
    ]

    lavagem_2 = lavagens[
        ordem_servico_com_lavagens["lavagem_2_id"]
    ]

    assert lavagem_1["ordem_servico_id"] == ordem_servico_id
    assert lavagem_1["status"] == "AGUARDANDO"
    assert lavagem_1["observacoes"] == "Lavagem OS teste 1"

    assert lavagem_2["ordem_servico_id"] == ordem_servico_id
    assert lavagem_2["status"] == "AGUARDANDO"
    assert lavagem_2["observacoes"] == "Lavagem OS teste 2"


def test_listar_lavagens_por_ordem_servico_retorna_lista_vazia(
    client,
    app_context,
):
    response = client.get(
        "/ordens-servico/999999/lavagens"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data == []


def test_listar_lavagens_por_ordem_servico_metodo_nao_permitido(
    client,
    ordem_servico_com_lavagens,
):
    ordem_servico_id = ordem_servico_com_lavagens["ordem_servico_id"]

    response = client.post(
        f"/ordens-servico/{ordem_servico_id}/lavagens"
    )

    assert response.status_code == 405