import uuid

import pytest

from app.extensions import db
from app.models import (
    Cliente,
    Lavagem,
    Marca,
    Modelo,
    OrdemServico,
    PorteVeiculo,
    Veiculo,
)
from app.repositories.lavagem_repository import LavagemRepository
from app.services.lavagem_service import LavagemService


@pytest.fixture
def ordem_servico(app_context):
    sufixo = uuid.uuid4().hex[:8]

    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=f"Cliente Integration {sufixo}",
        email=f"integration.{sufixo}@exemplo.com",
        telefone="48982222222",
    )

    marca = Marca(
        nome=f"Marca Integration {sufixo}",
    )

    porte = PorteVeiculo(
        nome=f"Porte Integration {sufixo}",
        ordem=93,
    )

    db.session.add_all([cliente, marca, porte])
    db.session.flush()

    modelo = Modelo(
        marca_id=marca.id,
        nome=f"Modelo Integration {sufixo}",
    )

    db.session.add(modelo)
    db.session.flush()

    veiculo = Veiculo(
        cliente_id=cliente.id,
        modelo_id=modelo.id,
        porte_id=porte.id,
        placa=f"INT{str(uuid.uuid4().int)[-4:]}",
        cor="Branco",
    )

    db.session.add(veiculo)
    db.session.flush()

    ordem = OrdemServico(
        numero=f"OS-INT-{sufixo}",
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
def test_fluxo_completo_da_lavagem(ordem_servico):
    lavagem = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status=LavagemService.STATUS_AGUARDANDO,
    )

    LavagemRepository.salvar(lavagem)
    db.session.commit()

    assert lavagem.id is not None
    assert lavagem.status == LavagemService.STATUS_AGUARDANDO

    LavagemService.iniciar(lavagem)
    db.session.commit()

    assert lavagem.status == LavagemService.STATUS_EM_ANDAMENTO
    assert lavagem.inicio is not None

    lavagem_db = LavagemRepository.buscar_por_id(lavagem.id)

    assert lavagem_db is not None
    assert lavagem_db.status == LavagemService.STATUS_EM_ANDAMENTO
    assert lavagem_db.inicio is not None

    LavagemService.concluir(lavagem_db)
    db.session.commit()

    assert lavagem_db.status == LavagemService.STATUS_CONCLUIDA
    assert lavagem_db.fim is not None

    lavagem_final = LavagemRepository.buscar_por_id(lavagem.id)

    assert lavagem_final is not None
    assert lavagem_final.status == LavagemService.STATUS_CONCLUIDA
    assert lavagem_final.inicio is not None
    assert lavagem_final.fim is not None


@pytest.mark.usefixtures("app_context")
def test_cancelamento_da_lavagem_persistido(ordem_servico):
    lavagem = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status=LavagemService.STATUS_AGUARDANDO,
    )

    LavagemRepository.salvar(lavagem)
    db.session.commit()

    LavagemService.cancelar(lavagem)
    db.session.commit()

    lavagem_db = LavagemRepository.buscar_por_id(lavagem.id)

    assert lavagem_db is not None
    assert lavagem_db.status == LavagemService.STATUS_CANCELADA