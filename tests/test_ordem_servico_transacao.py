from unittest.mock import patch

import pytest

from app.models.item_ordem_servico import ItemOrdemServico
from app.services.item_ordem_servico_service import (
    ItemOrdemServicoService,
)


def test_criar_item_ordem_servico_delega_para_repository():
    dados = {
        "ordem_servico_id": 10,
        "servico_id": 20,
        "quantidade": 2,
        "valor_unitario": 50.00,
        "desconto": 5.00,
        "tipo_desconto": "MANUAL",
    }

    with patch(
        "app.services.item_ordem_servico_service.ItemOrdemServicoRepository.salvar"
    ) as mock_salvar:
        mock_salvar.side_effect = lambda item: item

        resultado = ItemOrdemServicoService.criar(dados)

        mock_salvar.assert_called_once()

        item = mock_salvar.call_args.args[0]

        assert isinstance(item, ItemOrdemServico)
        assert item.ordem_servico_id == 10
        assert item.servico_id == 20
        assert item.quantidade == 2
        assert item.valor_unitario == 50.00
        assert item.desconto == 5.00
        assert item.tipo_desconto == "MANUAL"

        assert resultado is item


def test_criar_item_ordem_servico_aplica_quantidade_por_padrao():
    dados = {
        "ordem_servico_id": 10,
        "servico_id": 20,
        "valor_unitario": 50.00,
    }

    with patch(
        "app.services.item_ordem_servico_service.ItemOrdemServicoRepository.salvar"
    ) as mock_salvar:
        mock_salvar.side_effect = lambda item: item

        resultado = ItemOrdemServicoService.criar(dados)

        mock_salvar.assert_called_once()

        item = mock_salvar.call_args.args[0]

        assert isinstance(item, ItemOrdemServico)
        assert item.ordem_servico_id == 10
        assert item.servico_id == 20
        assert item.quantidade == 1
        assert item.valor_unitario == 50.00
        assert item.desconto == 0
        assert item.tipo_desconto == "NENHUM"

        assert resultado is item


def test_criar_item_ordem_servico_define_desconto_manual():
    dados = {
        "ordem_servico_id": 10,
        "servico_id": 20,
        "quantidade": 1,
        "valor_unitario": 50.00,
        "desconto": 10.00,
    }

    with patch(
        "app.services.item_ordem_servico_service.ItemOrdemServicoRepository.salvar"
    ) as mock_salvar:
        mock_salvar.side_effect = lambda item: item

        resultado = ItemOrdemServicoService.criar(dados)

        item = mock_salvar.call_args.args[0]

        assert resultado is item
        assert item.desconto == 10.00
        assert item.tipo_desconto == "MANUAL"


def test_criar_item_ordem_servico_rejeita_tipo_de_desconto_invalido():
    dados = {
        "ordem_servico_id": 10,
        "servico_id": 20,
        "quantidade": 1,
        "valor_unitario": 50.00,
        "desconto": 10.00,
        "tipo_desconto": "INVALIDO",
    }

    with pytest.raises(ValueError, match="Tipo de desconto inválido"):
        ItemOrdemServicoService.criar(dados)


def test_criar_item_ordem_servico_rejeita_desconto_sem_tipo_manual():
    dados = {
        "ordem_servico_id": 10,
        "servico_id": 20,
        "quantidade": 1,
        "valor_unitario": 50.00,
        "desconto": 10.00,
        "tipo_desconto": "NENHUM",
    }

    with pytest.raises(
        ValueError,
        match="Desconto monetário exige tipo de desconto MANUAL",
    ):
        ItemOrdemServicoService.criar(dados)


def test_criar_item_ordem_servico_rejeita_tipo_manual_sem_desconto():
    dados = {
        "ordem_servico_id": 10,
        "servico_id": 20,
        "quantidade": 1,
        "valor_unitario": 50.00,
        "desconto": 0,
        "tipo_desconto": "MANUAL",
    }

    with pytest.raises(
        ValueError,
        match="Tipo de desconto MANUAL exige desconto maior que zero",
    ):
        ItemOrdemServicoService.criar(dados)


def test_criar_item_ordem_servico_calcula_valor_bruto():
    item = ItemOrdemServico(
        ordem_servico_id=10,
        servico_id=20,
        quantidade=2,
        valor_unitario=50.00,
        desconto=5.00,
        tipo_desconto="MANUAL",
    )

    assert item.valor_bruto == 100.00


def test_criar_item_ordem_servico_calcula_valor_final():
    item = ItemOrdemServico(
        ordem_servico_id=10,
        servico_id=20,
        quantidade=2,
        valor_unitario=50.00,
        desconto=5.00,
        tipo_desconto="MANUAL",
    )

    assert item.valor_final == 95.00


def test_criar_item_ordem_servico_permite_desconto_de_cem_por_cento():
    item = ItemOrdemServico(
        ordem_servico_id=10,
        servico_id=20,
        quantidade=1,
        valor_unitario=50.00,
        desconto=50.00,
        tipo_desconto="MANUAL",
    )

    assert item.valor_bruto == 50.00
    assert item.valor_final == 0.00
    assert item.percentual_desconto == 100.00


def test_criar_item_ordem_servico_rejeita_valor_final_negativo():
    with pytest.raises(
        ValueError,
        match="O desconto não pode ser maior que o valor bruto",
    ):
        ItemOrdemServico(
            ordem_servico_id=10,
            servico_id=20,
            quantidade=1,
            valor_unitario=50.00,
            desconto=50.01,
            tipo_desconto="MANUAL",
        )


def test_buscar_item_ordem_servico_por_id_delega_para_repository():
    item = ItemOrdemServico(
        id=123,
        ordem_servico_id=10,
        servico_id=20,
        quantidade=1,
        valor_unitario=50.00,
        desconto=0,
    )

    with patch(
        "app.services.item_ordem_servico_service.ItemOrdemServicoRepository.buscar_por_id",
        return_value=item,
    ) as mock_buscar:
        resultado = ItemOrdemServicoService.buscar_por_id(123)

        mock_buscar.assert_called_once_with(123)

        assert resultado is item


def test_listar_itens_por_ordem_servico_delega_para_repository():
    itens = [
        ItemOrdemServico(
            id=1,
            ordem_servico_id=10,
            servico_id=20,
            quantidade=1,
            valor_unitario=40.00,
            desconto=0,
        ),
        ItemOrdemServico(
            id=2,
            ordem_servico_id=10,
            servico_id=21,
            quantidade=2,
            valor_unitario=50.00,
            desconto=5.00,
            tipo_desconto="MANUAL",
        ),
    ]

    with patch(
        "app.services.item_ordem_servico_service.ItemOrdemServicoRepository.listar_por_ordem_servico",
        return_value=itens,
    ) as mock_listar:
        resultado = (
            ItemOrdemServicoService.listar_por_ordem_servico(10)
        )

        mock_listar.assert_called_once_with(10)

        assert resultado is itens


def test_excluir_item_ordem_servico_delega_para_repository():
    item = ItemOrdemServico(
        id=123,
        ordem_servico_id=10,
        servico_id=20,
        quantidade=1,
        valor_unitario=50.00,
        desconto=0,
    )

    with patch(
        "app.services.item_ordem_servico_service.ItemOrdemServicoRepository.excluir"
    ) as mock_excluir:
        resultado = ItemOrdemServicoService.excluir(item)

        mock_excluir.assert_called_once_with(item)

        assert resultado is None