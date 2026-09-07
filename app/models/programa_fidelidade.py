from datetime import datetime, timezone

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db


class ProgramaFidelidade(db.Model):
    __tablename__ = "programas_fidelidade"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    nome: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    descricao: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    habilitado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    versao_configuracao: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
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

    configuracao = relationship(
        "ConfiguracaoFidelidade",
        back_populates="programa",
        uselist=False,
    )

    regras = relationship(
        "RegraFidelidade",
        back_populates="programa",
    )

    beneficios = relationship(
        "BeneficioFidelidade",
        back_populates="programa",
    )

    saldos = relationship(
        "SaldoFidelidade",
        back_populates="programa",
    )

    movimentacoes = relationship(
        "MovimentacaoFidelidade",
        back_populates="programa",
    )

    resgates = relationship(
        "ResgateFidelidade",
        back_populates="programa",
    )

    def __repr__(self) -> str:
        return f"<ProgramaFidelidade {self.id} - {self.nome}>"