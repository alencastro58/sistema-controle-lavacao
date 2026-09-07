from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class SaldoFidelidade(db.Model):
    __tablename__ = "saldos_fidelidade"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    programa_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("programas_fidelidade.id", ondelete="RESTRICT"),
        nullable=False,
    )

    cliente_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("clientes.id", ondelete="RESTRICT"),
        nullable=False,
    )

    saldo_pontos: Mapped[float] = mapped_column(
        Numeric(12, 4),
        nullable=False,
        default=0,
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    programa = relationship(
        "ProgramaFidelidade",
        back_populates="saldos",
    )

    cliente = relationship(
        "Cliente",
        back_populates="saldo_fidelidade",
    )

    movimentacoes = relationship(
        "MovimentacaoFidelidade",
        back_populates="saldo",
    )

    resgates = relationship(
        "ResgateFidelidade",
        back_populates="saldo",
    )

    def __repr__(self) -> str:
        return f"<SaldoFidelidade {self.id}>"
