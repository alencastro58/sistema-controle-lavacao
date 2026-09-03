from sqlalchemy import select

from ..extensions import db
from ..models.lavagem import Lavagem


class LavagemRepository:
    @staticmethod
    def salvar(lavagem: Lavagem) -> Lavagem:
        db.session.add(lavagem)
        db.session.flush()

        return lavagem

    @staticmethod
    def buscar_por_id(lavagem_id: int) -> Lavagem | None:
        return db.session.get(Lavagem, lavagem_id)

    @staticmethod
    def listar_todas() -> list[Lavagem]:
        stmt = (
            select(Lavagem)
            .order_by(Lavagem.id)
        )

        return list(db.session.scalars(stmt).all())

    @staticmethod
    def listar_por_ordem_servico(
        ordem_servico_id: int,
    ) -> list[Lavagem]:
        stmt = (
            select(Lavagem)
            .where(Lavagem.ordem_servico_id == ordem_servico_id)
            .order_by(Lavagem.id)
        )

        return list(db.session.scalars(stmt).all())

    @staticmethod
    def excluir(lavagem: Lavagem) -> None:
        db.session.delete(lavagem)
        db.session.flush()