from sqlalchemy import select

from ..extensions import db
from ..models.preco_servico import PrecoServico


class PrecoServicoRepository:
    @staticmethod
    def salvar(preco_servico: PrecoServico) -> PrecoServico:
        db.session.add(preco_servico)
        db.session.flush()

        return preco_servico

    @staticmethod
    def buscar_por_id(
        preco_servico_id: int,
    ) -> PrecoServico | None:
        return db.session.get(
            PrecoServico,
            preco_servico_id,
        )

    @staticmethod
    def listar_todos() -> list[PrecoServico]:
        stmt = (
            select(PrecoServico)
            .order_by(PrecoServico.id)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def listar_por_servico(
        servico_id: int,
    ) -> list[PrecoServico]:
        stmt = (
            select(PrecoServico)
            .where(
                PrecoServico.servico_id == servico_id
            )
            .order_by(PrecoServico.id)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def listar_por_porte(
        porte_id: int,
    ) -> list[PrecoServico]:
        stmt = (
            select(PrecoServico)
            .where(
                PrecoServico.porte_id == porte_id
            )
            .order_by(PrecoServico.id)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def excluir(
        preco_servico: PrecoServico,
    ) -> None:
        db.session.delete(preco_servico)
        db.session.flush()
