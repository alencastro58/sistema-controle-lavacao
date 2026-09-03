from sqlalchemy import select

from ..extensions import db
from ..models.ordem_servico import OrdemServico


class OrdemServicoRepository:
    @staticmethod
    def salvar(ordem_servico: OrdemServico) -> OrdemServico:
        db.session.add(ordem_servico)
        db.session.flush()

        return ordem_servico

    @staticmethod
    def buscar_por_id(
        ordem_servico_id: int,
    ) -> OrdemServico | None:
        return db.session.get(
            OrdemServico,
            ordem_servico_id,
        )

    @staticmethod
    def listar_todas() -> list[OrdemServico]:
        stmt = (
            select(OrdemServico)
            .order_by(OrdemServico.id)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def listar_por_cliente(
        cliente_id: int,
    ) -> list[OrdemServico]:
        stmt = (
            select(OrdemServico)
            .where(
                OrdemServico.cliente_id == cliente_id
            )
            .order_by(OrdemServico.id)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def listar_por_veiculo(
        veiculo_id: int,
    ) -> list[OrdemServico]:
        stmt = (
            select(OrdemServico)
            .where(
                OrdemServico.veiculo_id == veiculo_id
            )
            .order_by(OrdemServico.id)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def excluir(
        ordem_servico: OrdemServico,
    ) -> None:
        db.session.delete(ordem_servico)
        db.session.flush()
