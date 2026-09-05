from decimal import Decimal

from flask import has_app_context

from ..models.item_ordem_servico import ItemOrdemServico
from ..repositories.item_ordem_servico_repository import (
    ItemOrdemServicoRepository,
)
from ..repositories.ordem_servico_repository import (
    OrdemServicoRepository,
)
from ..repositories.preco_servico_repository import (
    PrecoServicoRepository,
)


class ItemOrdemServicoService:
    @staticmethod
    def recalcular_totais(ordem_servico) -> None:
        if ordem_servico is None:
            return

        ordem_servico.valor_total = sum(
            (item.valor_bruto for item in ordem_servico.itens),
            Decimal("0"),
        )

        ordem_servico.desconto = sum(
            (Decimal(str(item.desconto)) for item in ordem_servico.itens),
            Decimal("0"),
        )

    @staticmethod
    def criar(dados: dict) -> ItemOrdemServico:
        tipo_desconto = dados.get("tipo_desconto")
        desconto = dados.get("desconto", 0)

        if desconto is None:
            desconto = 0

        if tipo_desconto is not None and tipo_desconto not in {
            "NENHUM",
            "MANUAL",
        }:
            raise ValueError(
                "Tipo de desconto inválido (tipo_desconto)"
            )

        if tipo_desconto is None:
            tipo_desconto = (
                "MANUAL" if desconto > 0 else "NENHUM"
            )

        if desconto > 0 and tipo_desconto != "MANUAL":
            raise ValueError(
                "Desconto monetário exige tipo de desconto MANUAL"
            )

        if tipo_desconto == "MANUAL" and desconto <= 0:
            raise ValueError(
                "Tipo de desconto MANUAL exige desconto maior que zero"
            )

        valor_unitario = dados.get("valor_unitario")
        ordem_servico = None

        if valor_unitario is None:
            ordem_servico = OrdemServicoRepository.buscar_por_id(
                dados["ordem_servico_id"]
            )

            if ordem_servico is None:
                raise ValueError(
                    "Ordem de Serviço não encontrada."
                )

            porte_id = ordem_servico.veiculo.porte_id

            precos = PrecoServicoRepository.listar_por_servico(
                dados["servico_id"]
            )

            preco = next(
                (
                    item
                    for item in precos
                    if item.porte_id == porte_id
                    and item.ativo
                ),
                None,
            )

            if preco is None:
                raise ValueError(
                    "Não existe preço ativo para o serviço "
                    "e o porte do veículo."
                )

            valor_unitario = preco.valor

        item_ordem_servico = ItemOrdemServico(
            ordem_servico_id=dados["ordem_servico_id"],
            servico_id=dados["servico_id"],
            quantidade=dados.get("quantidade", 1),
            valor_unitario=valor_unitario,
            desconto=desconto,
            tipo_desconto=tipo_desconto,
        )

        item_ordem_servico = ItemOrdemServicoRepository.salvar(
            item_ordem_servico
        )

        if has_app_context():
            if ordem_servico is None:
                ordem_servico = OrdemServicoRepository.buscar_por_id(
                    dados["ordem_servico_id"]
                )

            ItemOrdemServicoService.recalcular_totais(ordem_servico)

        return item_ordem_servico

    @staticmethod
    def buscar_por_id(
        item_ordem_servico_id: int,
    ) -> ItemOrdemServico | None:
        return ItemOrdemServicoRepository.buscar_por_id(
            item_ordem_servico_id
        )

    @staticmethod
    def listar_por_ordem_servico(
        ordem_servico_id: int,
    ) -> list[ItemOrdemServico]:
        return ItemOrdemServicoRepository.listar_por_ordem_servico(
            ordem_servico_id
        )

    @staticmethod
    def excluir(
        item_ordem_servico: ItemOrdemServico,
    ) -> None:
        ordem_servico = item_ordem_servico.ordem_servico

        ItemOrdemServicoRepository.excluir(
            item_ordem_servico
        )

        if has_app_context():
            ItemOrdemServicoService.recalcular_totais(ordem_servico)
