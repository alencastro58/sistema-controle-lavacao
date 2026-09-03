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
def lavagem_existente(app_context):
    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social="Cliente Route Teste",
        email="route.teste@exemplo.com",
        telefone="48981111111",
    )

    marca = Marca(
        nome="Marca Route Teste",
    )

    porte = PorteVeiculo(
        nome="Porte Route Teste",
        ordem=92,
    )

    db.session.add_all([cliente, marca, porte])
    db.session.flush()

    modelo = Modelo(
        marca_id=marca.id,
        nome="Modelo Route Teste",
    )

    db.session.add(modelo)
    db.session.flush()

    veiculo = Veiculo(
        cliente_id=cliente.id,
        modelo_id=modelo.id,
        porte_id=porte.id,
        placa="ROT1234",
        cor="Branco",
    )

    db.session.add(veiculo)
    db.session.flush()

    ordem_servico = OrdemServico(
        numero="OS-ROUTE-001",
        cliente_id=cliente.id,
        veiculo_id=veiculo.id,
        valor_total=120,
        desconto=0,
        status="ABERTA",
    )

    db.session.add(ordem_servico)
    db.session.flush()

    lavagem = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status="AGUARDANDO",
        observacoes="Teste da rota de lavagem",
    )

    db.session.add(lavagem)
    db.session.commit()

    yield lavagem

    db.session.delete(lavagem)
    db.session.delete(ordem_servico)
    db.session.delete(veiculo)
    db.session.delete(modelo)
    db.session.delete(porte)
    db.session.delete(marca)
    db.session.delete(cliente)
    db.session.commit()


@pytest.mark.usefixtures("app_context")
def test_buscar_lavagem_existente(client, lavagem_existente):
    response = client.get(
        f"/lavagens/{lavagem_existente.id}"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == lavagem_existente.id
    assert data["ordem_servico_id"] == lavagem_existente.ordem_servico_id
    assert data["status"] == "AGUARDANDO"
    assert data["observacoes"] == "Teste da rota de lavagem"


def test_buscar_lavagem_inexistente(client):
    response = client.get("/lavagens/999999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["erro"] == "Lavagem não encontrada."


@pytest.mark.usefixtures("app_context")
def test_iniciar_lavagem_existente(client, lavagem_existente):
    response = client.post(
        f"/lavagens/{lavagem_existente.id}/iniciar"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == lavagem_existente.id
    assert data["status"] == "EM_ANDAMENTO"
    assert data["inicio"] is not None


def test_iniciar_lavagem_inexistente(client):
    response = client.post(
        "/lavagens/999999/iniciar"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["erro"] == "Lavagem não encontrada."


@pytest.mark.usefixtures("app_context")
def test_nao_permite_iniciar_lavagem_concluida(
    client,
    lavagem_existente,
):
    lavagem_existente.status = "CONCLUIDA"
    db.session.commit()

    response = client.post(
        f"/lavagens/{lavagem_existente.id}/iniciar"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert (
        data["erro"]
        == "Transição de status não permitida: "
        "CONCLUIDA -> EM_ANDAMENTO."
    )


@pytest.mark.usefixtures("app_context")
def test_concluir_lavagem_existente(
    client,
    lavagem_existente,
):
    lavagem_existente.status = "EM_ANDAMENTO"
    db.session.commit()

    response = client.post(
        f"/lavagens/{lavagem_existente.id}/concluir"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == lavagem_existente.id
    assert data["status"] == "CONCLUIDA"
    assert data["fim"] is not None


def test_concluir_lavagem_inexistente(client):
    response = client.post(
        "/lavagens/999999/concluir"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["erro"] == "Lavagem não encontrada."


@pytest.mark.usefixtures("app_context")
def test_nao_permite_concluir_lavagem_aguardando(
    client,
    lavagem_existente,
):
    response = client.post(
        f"/lavagens/{lavagem_existente.id}/concluir"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert (
        data["erro"]
        == "Transição de status não permitida: "
        "AGUARDANDO -> CONCLUIDA."
    )


@pytest.mark.usefixtures("app_context")
def test_cancelar_lavagem_aguardando(
    client,
    lavagem_existente,
):
    response = client.post(
        f"/lavagens/{lavagem_existente.id}/cancelar"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == lavagem_existente.id
    assert data["status"] == "CANCELADA"


@pytest.mark.usefixtures("app_context")
def test_cancelar_lavagem_em_andamento(
    client,
    lavagem_existente,
):
    lavagem_existente.status = "EM_ANDAMENTO"
    db.session.commit()

    response = client.post(
        f"/lavagens/{lavagem_existente.id}/cancelar"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == lavagem_existente.id
    assert data["status"] == "CANCELADA"


def test_cancelar_lavagem_inexistente(client):
    response = client.post(
        "/lavagens/999999/cancelar"
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["erro"] == "Lavagem não encontrada."


@pytest.mark.usefixtures("app_context")
def test_nao_permite_cancelar_lavagem_concluida(
    client,
    lavagem_existente,
):
    lavagem_existente.status = "CONCLUIDA"
    db.session.commit()

    response = client.post(
        f"/lavagens/{lavagem_existente.id}/cancelar"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert (
        data["erro"]
        == "Transição de status não permitida: "
        "CONCLUIDA -> CANCELADA."
    )


@pytest.mark.usefixtures("app_context")
def test_nao_permite_alterar_lavagem_cancelada(
    client,
    lavagem_existente,
):
    lavagem_existente.status = "CANCELADA"
    db.session.commit()

    response = client.post(
        f"/lavagens/{lavagem_existente.id}/iniciar"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert (
        data["erro"]
        == "Transição de status não permitida: "
        "CANCELADA -> EM_ANDAMENTO."
    )