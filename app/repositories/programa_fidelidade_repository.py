from sqlalchemy import select

from ..extensions import db
from ..models.programa_fidelidade import ProgramaFidelidade


class ProgramaFidelidadeRepository:
    @staticmethod
    def salvar(
        programa: ProgramaFidelidade,
    ) -> ProgramaFidelidade:
        db.session.add(programa)
        db.session.flush()

        return programa

    @staticmethod
    def buscar_por_id(
        programa_id: int,
    ) -> ProgramaFidelidade | None:
        return db.session.get(
            ProgramaFidelidade,
            programa_id,
        )

    @staticmethod
    def buscar_primeiro() -> ProgramaFidelidade | None:
        stmt = (
            select(ProgramaFidelidade)
            .order_by(ProgramaFidelidade.id)
            .limit(1)
        )

        return db.session.scalar(stmt)

    @staticmethod
    def listar_todos() -> list[ProgramaFidelidade]:
        stmt = (
            select(ProgramaFidelidade)
            .order_by(ProgramaFidelidade.id)
        )

        return list(
            db.session.scalars(stmt).all()
        )
