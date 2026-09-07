from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class MovimentacaoFidelidade(db.Model):
    __tablename__ = "movimentacoes_fidelidade"

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

    tipo: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    pontos: Mapped[float] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    saldo_anterior: Mapped[float] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    saldo_posterior: Mapped[float] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    regra_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("regras_fidelidade.id", ondelete="RESTRICT"),
        nullable=True,
    )

    beneficio_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("beneficios_fidelidade.id", ondelete="RESTRICT"),
        nullable=True,
    )

    versao_configuracao: Mapped[int] = mapped_column(
        nullable=False,
    )

    base_calculo: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    valor_base: Mapped[float | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    conversao_pontos: Mapped[float | None] = mapped_column(
        Numeric(12, 4),
        nullable=True,
    )

    validade_em: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
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

    programa = relationship(
        "ProgramaFidelidade",
        back_populates="movimentacoes",
    )

    cliente = relationship(
        "Cliente",
        back_populates="movimentacoes_fidelidade",
    )

    saldo = relationship(
        "SaldoFidelidade",
        back_populates="movimentacoes",
    )

    ordem_servico = relationship(
        "OrdemServico",
        back_populates="movimentacoes_fidelidade",
    )

    regra = relationship(
        "RegraFidelidade",
        back_populates="movimentacoes",
    )

    beneficio = relationship(
        "BeneficioFidelidade",
        back_populates="movimentacoes",
    )

    def __repr__(self) -> str:
        return f"<MovimentacaoFidelidade {self.id}>"
