from sqlalchemy import select

from ..extensions import db
from ..models.movimentacao_fidelidade import MovimentacaoFidelidade


class MovimentacaoFidelidadeRepository:
    @staticmethod
    def salvar(
        movimentacao: MovimentacaoFidelidade,
    ) -> MovimentacaoFidelidade:
        db.session.add(movimentacao)
        db.session.flush()

        return movimentacao

    @staticmethod
    def buscar_por_id(
        movimentacao_id: int,
    ) -> MovimentacaoFidelidade | None:
        return db.session.get(
            MovimentacaoFidelidade,
            movimentacao_id,
        )

    @staticmethod
    def buscar_por_ordem_servico(
        ordem_servico_id: int,
    ) -> list[MovimentacaoFidelidade]:
        stmt = (
            select(MovimentacaoFidelidade)
            .where(
                MovimentacaoFidelidade.ordem_servico_id
                == ordem_servico_id
            )
            .order_by(MovimentacaoFidelidade.id)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def buscar_credito_por_ordem_servico(
        ordem_servico_id: int,
    ) -> MovimentacaoFidelidade | None:
        stmt = (
            select(MovimentacaoFidelidade)
            .where(
                MovimentacaoFidelidade.ordem_servico_id
                == ordem_servico_id,
                MovimentacaoFidelidade.tipo == "CREDITO",
            )
            .limit(1)
        )

        return db.session.scalar(stmt)

    @staticmethod
    def listar_por_cliente(
        cliente_id: int,
    ) -> list[MovimentacaoFidelidade]:
        stmt = (
            select(MovimentacaoFidelidade)
            .where(
                MovimentacaoFidelidade.cliente_id
                == cliente_id
            )
            .order_by(MovimentacaoFidelidade.id)
        )

        return list(
            db.session.scalars(stmt).all()
        )
