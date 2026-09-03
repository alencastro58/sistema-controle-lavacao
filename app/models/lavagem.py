from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class Lavagem(db.Model):
    __tablename__ = "lavagens"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    ordem_servico_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("ordens_servico.id", ondelete="RESTRICT"),
        nullable=False,
    )

    inicio: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    fim: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="AGUARDANDO",
    )

    observacoes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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

    ordem_servico = relationship(
        "OrdemServico",
        back_populates="lavagens",
    )

    def __repr__(self) -> str:
        return f"<Lavagem {self.id} - OS {self.ordem_servico_id}>"
