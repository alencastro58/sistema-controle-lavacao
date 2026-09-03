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
def lavagens_existentes(app_context):
    identificador = uuid.uuid4().hex[:8]

    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=f"Cliente List Lavagem {identificador}",
        email=f"list.lavagem.{identificador}@exemplo.com",
        telefone="48980000002",
    )

    marca = Marca(
        nome=f"Marca List Lavagem {identificador}",
    )

    porte = PorteVeiculo(
        nome=f"Porte List Lavagem {identificador}",
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
        nome=f"Modelo List Lavagem {identificador}",
    )

    db.session.add(modelo)
    db.session.flush()

    veiculo = Veiculo(
        cliente_id=cliente.id,
        modelo_id=modelo.id,
        porte_id=porte.id,
        placa=f"L{identificador[:6]}",
        cor="Prata",
    )

    db.session.add(veiculo)
    db.session.flush()

    ordem_servico = OrdemServico(
        numero=f"OS-LIST-{identificador}",
        cliente_id=cliente.id,
        veiculo_id=veiculo.id,
        valor_total=200,
        desconto=0,
        status="ABERTA",
    )

    db.session.add(ordem_servico)
    db.session.flush()

    lavagem_1 = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status="AGUARDANDO",
        observacoes="Lavagem de teste 1",
    )

    lavagem_2 = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status="AGUARDANDO",
        observacoes="Lavagem de teste 2",
    )

    db.session.add_all(
        [
            lavagem_1,
            lavagem_2,
        ]
    )
    db.session.commit()

    lavagem_ids = [
        lavagem_1.id,
        lavagem_2.id,
    ]

    ordem_servico_id = ordem_servico.id
    veiculo_id = veiculo.id
    modelo_id = modelo.id
    porte_id = porte.id
    marca_id = marca.id
    cliente_id = cliente.id

    yield lavagem_ids

    db.session.rollback()

    for lavagem_id in lavagem_ids:
        lavagem = db.session.get(
            Lavagem,
            lavagem_id,
        )

        if lavagem is not None:
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


def test_listar_lavagens(
    client,
    lavagens_existentes,
):
    response = client.get("/lavagens")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) >= 2

    ids = [lavagem["id"] for lavagem in data]

    assert lavagens_existentes[0] in ids
    assert lavagens_existentes[1] in ids


def test_listar_lavagens_retorna_dados_da_lavagem(
    client,
    lavagens_existentes,
):
    response = client.get("/lavagens")

    assert response.status_code == 200

    data = response.get_json()

    lavagens = {
        lavagem["id"]: lavagem
        for lavagem in data
    }

    lavagem_1 = lavagens[lavagens_existentes[0]]
    lavagem_2 = lavagens[lavagens_existentes[1]]

    assert lavagem_1["status"] == "AGUARDANDO"
    assert lavagem_1["observacoes"] == "Lavagem de teste 1"

    assert lavagem_2["status"] == "AGUARDANDO"
    assert lavagem_2["observacoes"] == "Lavagem de teste 2"


def test_listar_lavagens_retorna_campos_padronizados(
    client,
    lavagens_existentes,
):
    response = client.get("/lavagens")

    assert response.status_code == 200

    data = response.get_json()

    lavagem = next(
        item
        for item in data
        if item["id"] == lavagens_existentes[0]
    )

    assert set(lavagem.keys()) == {
        "id",
        "ordem_servico_id",
        "inicio",
        "fim",
        "status",
        "observacoes",
        "criado_em",
        "atualizado_em",
    }


def test_listar_lavagens_metodo_nao_permitido(
    client,
):
    response = client.put("/lavagens")

    assert response.status_code == 405