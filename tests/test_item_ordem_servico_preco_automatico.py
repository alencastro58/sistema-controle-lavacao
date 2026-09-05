from decimal import Decimal

import pytest

from app.extensions import db
from app.models import PrecoServico
from app.services.item_ordem_servico_service import (
    ItemOrdemServicoService,
)


def test_criar_item_ordem_servico_forma_preco_automaticamente(
    dados_preco_automatico,
):
    dados = {
        "ordem_servico_id": dados_preco_automatico["ordem_servico_id"],
        "servico_id": dados_preco_automatico["servico_id"],
        "quantidade": 1,
    }

    item = ItemOrdemServicoService.criar(dados)

    assert item.valor_unitario == Decimal("125.00")


def test_preco_automatico_considera_o_porte_do_veiculo(
    dados_preco_automatico,
):
    dados = {
        "ordem_servico_id": dados_preco_automatico["ordem_servico_id"],
        "servico_id": dados_preco_automatico["servico_id"],
        "quantidade": 1,
    }

    item = ItemOrdemServicoService.criar(dados)

    preco = db.session.get(
        PrecoServico,
        dados_preco_automatico["preco_id"],
    )

    assert preco is not None
    assert preco.porte_id == dados_preco_automatico["porte_id"]
    assert item.valor_unitario == preco.valor


def test_preco_automatico_nao_deve_alterar_preco_cadastrado(
    dados_preco_automatico,
):
    preco_id = dados_preco_automatico["preco_id"]

    preco_antes = db.session.get(
        PrecoServico,
        preco_id,
    )

    assert preco_antes is not None
    assert preco_antes.valor == Decimal("125.00")

    dados = {
        "ordem_servico_id": dados_preco_automatico["ordem_servico_id"],
        "servico_id": dados_preco_automatico["servico_id"],
        "quantidade": 1,
    }

    ItemOrdemServicoService.criar(dados)

    preco_depois = db.session.get(
        PrecoServico,
        preco_id,
    )

    assert preco_depois is not None
    assert preco_depois.valor == Decimal("125.00")


def test_item_ordem_servico_pode_receber_valor_especifico_para_a_os(
    dados_preco_automatico,
):
    dados = {
        "ordem_servico_id": dados_preco_automatico["ordem_servico_id"],
        "servico_id": dados_preco_automatico["servico_id"],
        "quantidade": 1,
        "valor_unitario": 100.00,
    }

    item = ItemOrdemServicoService.criar(dados)

    assert item.valor_unitario == Decimal("100.00")

    preco = db.session.get(
        PrecoServico,
        dados_preco_automatico["preco_id"],
    )

    assert preco is not None
    assert preco.valor == Decimal("125.00")


def test_criar_item_ordem_servico_sem_preco_ativo_deve_ser_rejeitado(
    dados_preco_automatico,
):
    preco = db.session.get(
        PrecoServico,
        dados_preco_automatico["preco_id"],
    )

    assert preco is not None

    preco.ativo = False
    db.session.flush()

    dados = {
        "ordem_servico_id": dados_preco_automatico["ordem_servico_id"],
        "servico_id": dados_preco_automatico["servico_id"],
        "quantidade": 1,
    }

    with pytest.raises(ValueError, match="preço"):
        ItemOrdemServicoService.criar(dados)
