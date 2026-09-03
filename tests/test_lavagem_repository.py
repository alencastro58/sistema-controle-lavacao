import uuid

import pytest

from app.extensions import db
from app.models import (
    Cliente,
    Marca,
    Modelo,
    OrdemServico,
    PorteVeiculo,
    Veiculo,
    Lavagem,
)
from app.repositories.lavagem_repository import LavagemRepository


@pytest.fixture
def ordem_servico(app_context):
    sufixo = uuid.uuid4().hex[:8]

    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=f"Cliente Repository {sufixo}",
        email=f"teste.repository.{sufixo}@exemplo.com",
        telefone="48983333333",
    )

    marca = Marca(
        nome=f"Marca Repository {sufixo}",
    )

    porte = PorteVeiculo(
        nome=f"Porte Repository {sufixo}",
        ordem=94,
    )

    db.session.add_all([cliente, marca, porte])
    db.session.flush()

    modelo = Modelo(
        marca_id=marca.id,
        nome=f"Modelo Repository {sufixo}",
    )

    db.session.add(modelo)
    db.session.flush()

    veiculo = Veiculo(
        cliente_id=cliente.id,
        modelo_id=modelo.id,
        porte_id=porte.id,
        placa=f"REP{str(uuid.uuid4().int)[-4:]}",
        cor="Preto",
    )

    db.session.add(veiculo)
    db.session.flush()

    ordem = OrdemServico(
        numero=f"OS-REP-{sufixo}",
        cliente_id=cliente.id,
        veiculo_id=veiculo.id,
        valor_total=100.00,
        desconto=0,
        status="ABERTA",
    )

    db.session.add(ordem)
    db.session.flush()

    yield ordem

    db.session.rollback()

    db.session.query(Lavagem).filter(
        Lavagem.ordem_servico_id == ordem.id
    ).delete(synchronize_session=False)

    db.session.delete(ordem)
    db.session.delete(veiculo)
    db.session.delete(modelo)
    db.session.delete(porte)
    db.session.delete(marca)
    db.session.delete(cliente)

    db.session.commit()


@pytest.mark.usefixtures("app_context")
def test_salvar_lavagem(ordem_servico):
    lavagem = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status="AGUARDANDO",
    )

    LavagemRepository.salvar(lavagem)
    db.session.commit()

    assert lavagem.id is not None


@pytest.mark.usefixtures("app_context")
def test_buscar_lavagem_por_id(ordem_servico):
    lavagem = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status="AGUARDANDO",
    )

    LavagemRepository.salvar(lavagem)
    db.session.commit()

    encontrada = LavagemRepository.buscar_por_id(lavagem.id)

    assert encontrada is not None
    assert encontrada.id == lavagem.id


@pytest.mark.usefixtures("app_context")
def test_listar_lavagens_por_ordem_servico(ordem_servico):
    lavagem_1 = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status="AGUARDANDO",
    )

    lavagem_2 = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status="AGUARDANDO",
    )

    LavagemRepository.salvar(lavagem_1)
    LavagemRepository.salvar(lavagem_2)
    db.session.commit()

    lista = LavagemRepository.listar_por_ordem_servico(
        ordem_servico.id
    )

    assert len(lista) == 2
    assert {lavagem.id for lavagem in lista} == {
        lavagem_1.id,
        lavagem_2.id,
    }


@pytest.mark.usefixtures("app_context")
def test_excluir_lavagem(ordem_servico):
    lavagem = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status="AGUARDANDO",
    )

    LavagemRepository.salvar(lavagem)
    db.session.commit()

    lavagem_id = lavagem.id

    LavagemRepository.excluir(lavagem)
    db.session.commit()

    restante = LavagemRepository.buscar_por_id(lavagem_id)

    assert restante is None