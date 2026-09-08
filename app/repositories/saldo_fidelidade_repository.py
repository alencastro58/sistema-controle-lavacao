from sqlalchemy import select

from ..extensions import db
from ..models.saldo_fidelidade import SaldoFidelidade


class SaldoFidelidadeRepository:
    @staticmethod
    def salvar(
        saldo: SaldoFidelidade,
    ) -> SaldoFidelidade:
        db.session.add(saldo)
        db.session.flush()

        return saldo

    @staticmethod
    def buscar_por_id(
        saldo_id: int,
    ) -> SaldoFidelidade | None:
        return db.session.get(
            SaldoFidelidade,
            saldo_id,
        )

    @staticmethod
    def buscar_por_programa_e_cliente(
        programa_id: int,
        cliente_id: int,
    ) -> SaldoFidelidade | None:
        stmt = (
            select(SaldoFidelidade)
            .where(
                SaldoFidelidade.programa_id == programa_id,
                SaldoFidelidade.cliente_id == cliente_id,
            )
        )

        return db.session.scalar(stmt)
