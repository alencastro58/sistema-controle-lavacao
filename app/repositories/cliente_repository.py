from sqlalchemy import select

from ..extensions import db
from ..models.cliente import Cliente


class ClienteRepository:
    @staticmethod
    def salvar(cliente: Cliente) -> Cliente:
        db.session.add(cliente)
        db.session.flush()

        return cliente

    @staticmethod
    def buscar_por_id(
        cliente_id: int,
    ) -> Cliente | None:
        return db.session.get(
            Cliente,
            cliente_id,
        )

    @staticmethod
    def buscar_por_cpf_cnpj(
        cpf_cnpj: str,
    ) -> Cliente | None:
        stmt = (
            select(Cliente)
            .where(
                Cliente.cpf_cnpj == cpf_cnpj
            )
        )

        return db.session.scalar(stmt)

    @staticmethod
    def listar_todos() -> list[Cliente]:
        stmt = (
            select(Cliente)
            .order_by(Cliente.id)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def listar_ativos() -> list[Cliente]:
        stmt = (
            select(Cliente)
            .where(
                Cliente.ativo.is_(True)
            )
            .order_by(Cliente.nome_razao_social)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def excluir(
        cliente: Cliente,
    ) -> None:
        db.session.delete(cliente)
        db.session.flush()