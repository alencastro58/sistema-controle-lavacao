pytest_plugins = ["tests.test_lavagem_integration"]
import uuid

import pytest

from app import create_app
from app.extensions import db
from app.models import (
    Cliente,
    ItemOrdemServico,
    Marca,
    Modelo,
    OrdemServico,
    PorteVeiculo,
    PrecoServico,
    Servico,
    Veiculo,
)


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def app_context(app):
    with app.app_context():
        yield


@pytest.fixture
def dados_preco_automatico(app_context):
    sufixo = uuid.uuid4().hex[:8]

    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=f"Cliente Preco Automatico {sufixo}",
        email=f"cliente.preco.automatico.{sufixo}@exemplo.com",
        telefone="48985555555",
    )

    marca = Marca(
        nome=f"Marca Preco Automatico {sufixo}",
    )

    porte = PorteVeiculo(
        nome=f"Porte Preco Automatico {sufixo}",
        ordem=99,
    )

    servico = Servico(
        nome=f"Servico Preco Automatico {sufixo}",
        descricao="Servico para teste de formacao automatica de preco",
        valor=0,
        ativo=True,
    )

    db.session.add_all(
        [
            cliente,
            marca,
            porte,
            servico,
        ]
    )
    db.session.flush()

    modelo = Modelo(
        marca_id=marca.id,
        nome=f"Modelo Preco Automatico {sufixo}",
    )

    db.session.add(modelo)
    db.session.flush()

    veiculo = Veiculo(
        cliente_id=cliente.id,
        modelo_id=modelo.id,
        porte_id=porte.id,
        placa=f"PAT{str(uuid.uuid4().int)[-4:]}",
        cor="Preto",
    )

    db.session.add(veiculo)
    db.session.flush()

    ordem = OrdemServico(
        numero=f"OS-PRECO-{sufixo}",
        cliente_id=cliente.id,
        veiculo_id=veiculo.id,
        valor_total=0,
        desconto=0,
        status="ABERTA",
    )

    db.session.add(ordem)
    db.session.flush()

    preco = PrecoServico(
        servico_id=servico.id,
        porte_id=porte.id,
        valor=125.00,
        ativo=True,
    )

    db.session.add(preco)
    db.session.commit()

    dados = {
        "cliente_id": cliente.id,
        "marca_id": marca.id,
        "modelo_id": modelo.id,
        "porte_id": porte.id,
        "veiculo_id": veiculo.id,
        "servico_id": servico.id,
        "ordem_servico_id": ordem.id,
        "preco_id": preco.id,
    }

    yield dados

    db.session.rollback()

    preco = db.session.get(
        PrecoServico,
        dados["preco_id"],
    )
    if preco is not None:
        db.session.delete(preco)

    ordem = db.session.get(
        OrdemServico,
        dados["ordem_servico_id"],
    )
    if ordem is not None:
        db.session.delete(ordem)

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

    cliente = db.session.get(
        Cliente,
        dados["cliente_id"],
    )
    if cliente is not None:
        db.session.delete(cliente)

    db.session.commit()

