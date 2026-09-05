from datetime import datetime, timezone

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class PrecoServico(db.Model):
    __tablename__ = "precos_servicos"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    servico_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("servicos.id", ondelete="RESTRICT"),
        nullable=False,
    )

    porte_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("portes_veiculo.id", ondelete="RESTRICT"),
        nullable=False,
    )

    valor: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
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

    servico = relationship(
        "Servico",
        back_populates="precos",
    )

    porte = relationship(
        "PorteVeiculo",
        back_populates="precos_servicos",
    )

    __table_args__ = (
        db.UniqueConstraint(
            "servico_id",
            "porte_id",
            name="uq_precos_servicos_servico_porte",
        ),
    )

    def __repr__(self) -> str:
        return f"<PrecoServico {self.id}>"