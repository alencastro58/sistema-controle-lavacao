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


class RegraFidelidade(db.Model):
    __tablename__ = "regras_fidelidade"

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

    servico_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("servicos.id", ondelete="RESTRICT"),
        nullable=True,
    )

    nome: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    tipo_regra: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    prioridade: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    base_calculo: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    tipo_pontos: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    arredondamento: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    pontos_fixos: Mapped[float | None] = mapped_column(
        Numeric(12, 4),
        nullable=True,
    )

    valor_por_ponto: Mapped[float | None] = mapped_column(
        Numeric(12, 4),
        nullable=True,
    )

    pontos_por_valor: Mapped[float | None] = mapped_column(
        Numeric(12, 4),
        nullable=True,
    )

    valor_minimo: Mapped[float | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    valor_maximo: Mapped[float | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
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
        back_populates="regras",
    )

    servico = relationship(
        "Servico",
        back_populates="regras_fidelidade",
    )

    movimentacoes = relationship(
        "MovimentacaoFidelidade",
        back_populates="regra",
    )

    def __repr__(self) -> str:
        return f"<RegraFidelidade {self.id}>"
