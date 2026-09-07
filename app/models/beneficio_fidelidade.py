from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class BeneficioFidelidade(db.Model):
    __tablename__ = "beneficios_fidelidade"

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

    nome: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    custo_pontos: Mapped[float] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    valor_monetario: Mapped[float | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    servico_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("servicos.id", ondelete="RESTRICT"),
        nullable=True,
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    validade_tipo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    validade_dias: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    validade_data: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    prazo_utilizacao_tipo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    prazo_utilizacao_dias: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    permite_pagamento_integral: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    politica_debito: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    politica_expiracao: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
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
        back_populates="beneficios",
    )

    servico = relationship(
        "Servico",
        back_populates="beneficios_fidelidade",
    )

    movimentacoes = relationship(
        "MovimentacaoFidelidade",
        back_populates="beneficio",
    )

    resgates = relationship(
        "ResgateFidelidade",
        back_populates="beneficio",
    )

    def __repr__(self) -> str:
        return f"<BeneficioFidelidade {self.id}>"
