import uuid

import pytest

from app.extensions import db
from app.models import ItemOrdemServico, Servico
from app.repositories.item_ordem_servico_repository import (
    ItemOrdemServicoRepository,
)
from app.services.item_ordem_servico_service import ItemOrdemServicoService


@pytest.fixture
def servicos(app_context):
    sufixo = uuid.uuid4().hex[:8]

    servico_1 = Servico(
        nome=f"Servico Integracao 1 {sufixo}",
        descricao="Servico para teste de persistencia",
        valor=0,
        ativo=True,
    )

    servico_2 = Servico(
        nome=f"Servico Integracao 2 {sufixo}",
        descricao="Servico para teste de persistencia",
        valor=0,
        ativo=True,
    )

    db.session.add_all([servico_1, servico_2])
    db.session.commit()

    yield servico_1, servico_2

    db.session.rollback()

    for servico in (servico_1, servico_2):
        servico_db = db.session.get(Servico, servico.id)
        if servico_db is not None:
            db.session.delete(servico_db)

    db.session.commit()


@pytest.mark.usefixtures("app_context")
def test_persistencia_e_recalculo_financeiro_dos_itens(
    ordem_servico,
    servicos,
):
    servico_1, servico_2 = servicos

    item_1 = ItemOrdemServicoService.criar(
        {
            "ordem_servico_id": ordem_servico.id,
            "servico_id": servico_1.id,
            "quantidade": 2,
            "valor_unitario": 50.00,
            "desconto": 5.00,
            "tipo_desconto": "MANUAL",
        }
    )

    db.session.commit()

    ordem_db = db.session.get(type(ordem_servico), ordem_servico.id)

    assert item_1.id is not None
    assert ordem_db.valor_total == 100.00
    assert ordem_db.desconto == 5.00

    item_2 = ItemOrdemServicoService.criar(
        {
            "ordem_servico_id": ordem_servico.id,
            "servico_id": servico_2.id,
            "quantidade": 1,
            "valor_unitario": 80.00,
            "desconto": 10.00,
            "tipo_desconto": "MANUAL",
        }
    )

    db.session.commit()

    ordem_db = db.session.get(type(ordem_servico), ordem_servico.id)

    assert item_2.id is not None
    assert ordem_db.valor_total == 180.00
    assert ordem_db.desconto == 15.00

    ItemOrdemServicoService.excluir(item_1)
    db.session.commit()

    ordem_db = db.session.get(type(ordem_servico), ordem_servico.id)

    assert ordem_db.valor_total == 80.00
    assert ordem_db.desconto == 10.00

    item_2_db = ItemOrdemServicoRepository.buscar_por_id(item_2.id)

    ItemOrdemServicoService.excluir(item_2_db)
    db.session.commit()

    ordem_db = db.session.get(type(ordem_servico), ordem_servico.id)

    assert ordem_db.valor_total == 0.00
    assert ordem_db.desconto == 0.00
