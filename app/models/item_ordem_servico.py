from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class ItemOrdemServico(db.Model):
    __tablename__ = "itens_ordem_servico"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    ordem_servico_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("ordens_servico.id", ondelete="CASCADE"),
        nullable=False,
    )

    servico_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("servicos.id", ondelete="RESTRICT"),
        nullable=False,
    )

    quantidade: Mapped[int] = mapped_column(
        db.Integer,
        nullable=False,
        default=1,
    )

    valor_unitario: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    desconto: Mapped[float] = mapped_column(
        Numeric(12, 2),
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

    ordem_servico = relationship(
        "OrdemServico",
        back_populates="itens",
    )

    servico = relationship(
        "Servico",
        back_populates="itens_ordem_servico",
    )

    def __repr__(self) -> str:
        return f"<ItemOrdemServico {self.id}>"
