from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class ConfiguracaoFidelidade(db.Model):
    __tablename__ = "configuracoes_fidelidade"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    programa_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("programas_fidelidade.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )

    evento_geracao: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    base_calculo_padrao: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    tipo_pontos_padrao: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    arredondamento_padrao: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    validade_tipo_padrao: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    validade_dias_padrao: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    validade_data_padrao: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    permite_desconto_monetario: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    permite_beneficios: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    permite_os_geradora: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    permite_pagamento_integral: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    limite_percentual_os: Mapped[float | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    limite_monetario_os: Mapped[float | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    politica_estorno: Mapped[str] = mapped_column(
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
        back_populates="configuracao",
    )

    def __repr__(self) -> str:
        return f"<ConfiguracaoFidelidade {self.id}>"