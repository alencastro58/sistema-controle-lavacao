from datetime import datetime, timezone

from sqlalchemy import BigInteger, Boolean, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class ProgramaFidelidade(db.Model):
    __tablename__ = "programas_fidelidade"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    habilitado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    pontos_por_real: Mapped[float] = mapped_column(
        Numeric(12, 4),
        nullable=False,
        default=1,
    )

    valor_por_ponto: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=1,
    )

    desconto_maximo_percentual: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=100,
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

    saldos = relationship(
        "SaldoFidelidade",
        back_populates="programa",
    )

    movimentacoes = relationship(
        "MovimentacaoFidelidade",
        back_populates="programa",
    )

    def __repr__(self) -> str:
        return f"<ProgramaFidelidade {self.id}>"