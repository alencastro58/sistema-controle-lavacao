from sqlalchemy import select

from ..extensions import db
from ..models.preco_servico import PrecoServico


class PrecoServicoRepository:
    @staticmethod
    def salvar(preco: PrecoServico) -> PrecoServico:
        db.session.add(preco)
        db.session.flush()

        return preco

    @staticmethod
    def buscar_por_id(
        preco_id: int,
    ) -> PrecoServico | None:
        return db.session.get(
            PrecoServico,
            preco_id,
        )

    @staticmethod
    def buscar_por_servico_e_porte(
        servico_id: int,
        porte_id: int,
    ) -> PrecoServico | None:
        stmt = (
            select(PrecoServico)
            .where(
                PrecoServico.servico_id == servico_id,
                PrecoServico.porte_id == porte_id,
                PrecoServico.ativo.is_(True),
            )
        )

        return db.session.scalar(stmt)

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
        preco: PrecoServico,
    ) -> None:
        db.session.delete(preco)
        db.session.flush()