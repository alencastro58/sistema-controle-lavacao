from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class ResgateFidelidade(db.Model):
    __tablename__ = "resgates_fidelidade"

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

    saldo_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("saldos_fidelidade.id", ondelete="RESTRICT"),
        nullable=False,
    )

    ordem_servico_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("ordens_servico.id", ondelete="RESTRICT"),
        nullable=True,
    )

    beneficio_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("beneficios_fidelidade.id", ondelete="RESTRICT"),
        nullable=True,
    )

    modalidade: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    pontos_solicitados: Mapped[float] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    pontos_debitados: Mapped[float] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    valor_desconto: Mapped[float | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    conversao_pontos: Mapped[float | None] = mapped_column(
        Numeric(12, 4),
        nullable=True,
    )

    data_solicitacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    data_aprovacao: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    data_utilizacao: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    data_cancelamento: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    data_expiracao: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    versao_configuracao: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    descricao: Mapped[str | None] = mapped_column(
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

    programa = relationship(
        "ProgramaFidelidade",
        back_populates="resgates",
    )

    cliente = relationship(
        "Cliente",
        back_populates="resgates_fidelidade",
    )

    saldo = relationship(
        "SaldoFidelidade",
        back_populates="resgates",
    )

    ordem_servico = relationship(
        "OrdemServico",
        back_populates="resgates_fidelidade",
    )

    beneficio = relationship(
        "BeneficioFidelidade",
        back_populates="resgates",
    )

    def __repr__(self) -> str:
        return f"<ResgateFidelidade {self.id}>"
