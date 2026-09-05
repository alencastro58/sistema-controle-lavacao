from sqlalchemy import select

from ..extensions import db
from ..models.item_ordem_servico import ItemOrdemServico


class ItemOrdemServicoRepository:
    @staticmethod
    def salvar(
        item_ordem_servico: ItemOrdemServico,
    ) -> ItemOrdemServico:
        db.session.add(item_ordem_servico)
        db.session.flush()

        return item_ordem_servico

    @staticmethod
    def buscar_por_id(
        item_ordem_servico_id: int,
    ) -> ItemOrdemServico | None:
        return db.session.get(
            ItemOrdemServico,
            item_ordem_servico_id,
        )

    @staticmethod
    def listar_por_ordem_servico(
        ordem_servico_id: int,
    ) -> list[ItemOrdemServico]:
        stmt = (
            select(ItemOrdemServico)
            .where(
                ItemOrdemServico.ordem_servico_id
                == ordem_servico_id
            )
            .order_by(ItemOrdemServico.id)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def excluir(
        item_ordem_servico: ItemOrdemServico,
    ) -> None:
        db.session.delete(item_ordem_servico)
        db.session.flush()
