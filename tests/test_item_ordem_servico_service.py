from unittest.mock import patch

import pytest

from app.models.item_ordem_servico import ItemOrdemServico
from app.services.item_ordem_servico_service import (
    ItemOrdemServicoService,
)


class TestItemOrdemServicoService:
    def test_criar_item_define_desconto_manual(self):
        dados = {
            "ordem_servico_id": 1,
            "servico_id": 2,
            "quantidade": 1,
            "valor_unitario": 100,
            "desconto": 20,
        }

        with patch(
            "app.services.item_ordem_servico_service."
            "ItemOrdemServicoRepository.salvar"
        ) as mock_salvar:
            ItemOrdemServicoService.criar(dados)

        item = mock_salvar.call_args.args[0]

        assert item.tipo_desconto == "MANUAL"

    def test_criar_item_sem_desconto_define_nenhum(self):
        dados = {
            "ordem_servico_id": 1,
            "servico_id": 2,
            "quantidade": 1,
            "valor_unitario": 100,
        }

        with patch(
            "app.services.item_ordem_servico_service."
            "ItemOrdemServicoRepository.salvar"
        ) as mock_salvar:
            ItemOrdemServicoService.criar(dados)

        item = mock_salvar.call_args.args[0]

        assert item.tipo_desconto == "NENHUM"

    def test_criar_item_rejeita_tipo_desconto_invalido(self):
        dados = {
            "ordem_servico_id": 1,
            "servico_id": 2,
            "quantidade": 1,
            "valor_unitario": 100,
            "desconto": 20,
            "tipo_desconto": "INVALIDO",
        }

        with pytest.raises(ValueError, match="tipo_desconto"):
            ItemOrdemServicoService.criar(dados)

    def test_criar_item_rejeita_desconto_negativo(self):
        dados = {
            "ordem_servico_id": 1,
            "servico_id": 2,
            "quantidade": 1,
            "valor_unitario": 100,
            "desconto": -1,
        }

        with pytest.raises(ValueError, match="desconto"):
            ItemOrdemServicoService.criar(dados)

    def test_criar_item_rejeita_desconto_maior_que_valor_bruto(self):
        dados = {
            "ordem_servico_id": 1,
            "servico_id": 2,
            "quantidade": 1,
            "valor_unitario": 100,
            "desconto": 101,
        }

        with pytest.raises(ValueError, match="desconto"):
            ItemOrdemServicoService.criar(dados)

    def test_valor_bruto(self):
        item = ItemOrdemServico(
            ordem_servico_id=1,
            servico_id=2,
            quantidade=3,
            valor_unitario=100,
            desconto=20,
        )

        assert item.valor_bruto == 300

    def test_valor_final(self):
        item = ItemOrdemServico(
            ordem_servico_id=1,
            servico_id=2,
            quantidade=3,
            valor_unitario=100,
            desconto=20,
        )

        assert item.valor_final == 280

    def test_percentual_desconto(self):
        item = ItemOrdemServico(
            ordem_servico_id=1,
            servico_id=2,
            quantidade=2,
            valor_unitario=100,
            desconto=20,
        )

        assert item.percentual_desconto == 10

    def test_percentual_desconto_sem_valor_bruto(self):
        item = ItemOrdemServico(
            ordem_servico_id=1,
            servico_id=2,
            quantidade=1,
            valor_unitario=0,
            desconto=0,
        )

        assert item.percentual_desconto == 0

    def test_criar_item_com_valor_unitario_manual(self):
        dados = {
            "ordem_servico_id": 1,
            "servico_id": 2,
            "quantidade": 1,
            "valor_unitario": 150,
        }

        with patch(
            "app.services.item_ordem_servico_service."
            "ItemOrdemServicoRepository.salvar"
        ) as mock_salvar:
            ItemOrdemServicoService.criar(dados)

        item = mock_salvar.call_args.args[0]

        assert item.valor_unitario == 150

    def test_criar_item_com_quantidade_padrao(self):
        dados = {
            "ordem_servico_id": 1,
            "servico_id": 2,
            "valor_unitario": 100,
        }

        with patch(
            "app.services.item_ordem_servico_service."
            "ItemOrdemServicoRepository.salvar"
        ) as mock_salvar:
            ItemOrdemServicoService.criar(dados)

        item = mock_salvar.call_args.args[0]

        assert item.quantidade == 1

    def test_criar_item_com_desconto_zero(self):
        dados = {
            "ordem_servico_id": 1,
            "servico_id": 2,
            "quantidade": 1,
            "valor_unitario": 100,
            "desconto": 0,
        }

        with patch(
            "app.services.item_ordem_servico_service."
            "ItemOrdemServicoRepository.salvar"
        ) as mock_salvar:
            ItemOrdemServicoService.criar(dados)

        item = mock_salvar.call_args.args[0]

        assert item.desconto == 0
        assert item.tipo_desconto == "NENHUM"
