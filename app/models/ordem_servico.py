from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class OrdemServico(db.Model):
    __tablename__ = "ordens_servico"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    numero: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    cliente_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("clientes.id", ondelete="RESTRICT"),
        nullable=False,
    )

    veiculo_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("veiculos.id", ondelete="RESTRICT"),
        nullable=False,
    )

    data_agendamento: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    valor_total: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    desconto: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ABERTA",
    )

    pagamento_confirmado: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    pagamento_confirmado_em: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    veiculo_entregue: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    veiculo_entregue_em: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
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

    cliente = relationship(
        "Cliente",
        back_populates="ordens_servico",
    )

    veiculo = relationship(
        "Veiculo",
        back_populates="ordens_servico",
    )

    itens = relationship(
        "ItemOrdemServico",
        back_populates="ordem_servico",
        cascade="all, delete-orphan",
    )

    lavagens = relationship(
        "Lavagem",
        back_populates="ordem_servico",
    )
