from decimal import Decimal
from unittest.mock import patch

from app.models.item_ordem_servico import ItemOrdemServico
from app.services.item_ordem_servico_service import (
    ItemOrdemServicoService,
)


def test_recalcular_ordem_servico_soma_valores_brutos_e_descontos():
    item_1 = ItemOrdemServico(
        ordem_servico_id=1,
        servico_id=1,
        quantidade=2,
        valor_unitario=100,
        desconto=10,
    )

    item_2 = ItemOrdemServico(
        ordem_servico_id=1,
        servico_id=2,
        quantidade=1,
        valor_unitario=50,
        desconto=5,
    )

    ordem_servico = type(
        "OrdemServicoFake",
        (),
        {
            "itens": [item_1, item_2],
            "valor_total": Decimal("0"),
            "desconto": Decimal("0"),
        },
    )()

    ItemOrdemServicoService.recalcular_totais(ordem_servico)

    assert ordem_servico.valor_total == Decimal("250")
    assert ordem_servico.desconto == Decimal("15")


def test_recalcular_ordem_servico_sem_itens_zera_totais():
    ordem_servico = type(
        "OrdemServicoFake",
        (),
        {
            "itens": [],
            "valor_total": Decimal("100"),
            "desconto": Decimal("20"),
        },
    )()

    ItemOrdemServicoService.recalcular_totais(ordem_servico)

    assert ordem_servico.valor_total == Decimal("0")
    assert ordem_servico.desconto == Decimal("0")
