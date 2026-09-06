from sqlalchemy import select

from ..extensions import db
from ..models.veiculo import Veiculo


class VeiculoRepository:
    @staticmethod
    def salvar(veiculo: Veiculo) -> Veiculo:
        db.session.add(veiculo)
        db.session.flush()

        return veiculo

    @staticmethod
    def buscar_por_id(
        veiculo_id: int,
    ) -> Veiculo | None:
        return db.session.get(
            Veiculo,
            veiculo_id,
        )

    @staticmethod
    def buscar_por_placa(
        placa: str,
    ) -> Veiculo | None:
        stmt = (
            select(Veiculo)
            .where(
                Veiculo.placa == placa
            )
        )

        return db.session.scalar(stmt)

    @staticmethod
    def listar_todos() -> list[Veiculo]:
        stmt = (
            select(Veiculo)
            .order_by(Veiculo.id)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def listar_ativos() -> list[Veiculo]:
        stmt = (
            select(Veiculo)
            .where(
                Veiculo.ativo.is_(True)
            )
            .order_by(Veiculo.placa)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def listar_por_cliente(
        cliente_id: int,
    ) -> list[Veiculo]:
        stmt = (
            select(Veiculo)
            .where(
                Veiculo.cliente_id == cliente_id
            )
            .order_by(Veiculo.placa)
        )

        return list(
            db.session.scalars(stmt).all()
        )

    @staticmethod
    def excluir(
        veiculo: Veiculo,
    ) -> None:
        db.session.delete(veiculo)
        db.session.flush()
