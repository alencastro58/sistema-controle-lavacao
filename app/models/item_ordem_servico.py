from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, String
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

    valor_unitario: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    desconto: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    tipo_desconto: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="NENHUM",
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

    def __init__(self, **kwargs):
        tipo_desconto = kwargs.get("tipo_desconto")

        if tipo_desconto is None:
            desconto = Decimal(
                str(kwargs.get("desconto", 0))
            )

            tipo_desconto = (
                "MANUAL"
                if desconto > 0
                else "NENHUM"
            )

            kwargs["tipo_desconto"] = tipo_desconto

        if tipo_desconto not in {"NENHUM", "MANUAL"}:
            raise ValueError(
                "tipo_desconto deve ser NENHUM ou MANUAL."
            )

        quantidade = kwargs.get("quantidade", 1)

        if quantidade <= 0:
            raise ValueError(
                "A quantidade deve ser maior que zero."
            )

        desconto = Decimal(
            str(kwargs.get("desconto", 0))
        )

        if desconto < 0:
            raise ValueError(
                "O desconto não pode ser negativo."
            )

        valor_unitario = kwargs.get("valor_unitario")

        if valor_unitario is not None:
            valor_bruto = (
                Decimal(str(quantidade))
                * Decimal(str(valor_unitario))
            )

            if desconto > valor_bruto:
                raise ValueError(
                    "O desconto não pode ser maior que "
                    "o valor bruto do item."
                )

        super().__init__(**kwargs)

    @property
    def valor_bruto(self) -> Decimal:
        return (
            Decimal(str(self.quantidade))
            * Decimal(str(self.valor_unitario))
        )

    @property
    def valor_final(self) -> Decimal:
        valor_final = (
            self.valor_bruto
            - Decimal(str(self.desconto))
        )

        if valor_final < 0:
            raise ValueError(
                "O valor final não pode ser negativo."
            )

        return valor_final

    @property
    def percentual_desconto(self) -> Decimal:
        if self.valor_bruto == 0:
            return Decimal("0")

        return (
            Decimal(str(self.desconto))
            / self.valor_bruto
            * Decimal("100")
        )

    def __repr__(self) -> str:
        return f"<ItemOrdemServico {self.id}>"
