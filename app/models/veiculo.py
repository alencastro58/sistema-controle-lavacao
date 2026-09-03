from datetime import datetime, timezone

from app.extensions import db


class Veiculo(db.Model):
    __tablename__ = "veiculos"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    cliente_id = db.Column(
        db.BigInteger,
        db.ForeignKey("clientes.id", ondelete="RESTRICT"),
        nullable=False,
    )

    modelo_id = db.Column(
        db.BigInteger,
        db.ForeignKey("modelos.id", ondelete="RESTRICT"),
        nullable=False,
    )

    porte_id = db.Column(
        db.BigInteger,
        db.ForeignKey("portes_veiculo.id", ondelete="RESTRICT"),
        nullable=False,
    )

    placa = db.Column(db.String(10), nullable=False, unique=True)

    cor = db.Column(db.String(50), nullable=False)

    ano_fabricacao = db.Column(db.SmallInteger, nullable=True)

    ano_modelo = db.Column(db.SmallInteger, nullable=True)

    renavam = db.Column(db.String(11), nullable=True)

    chassi = db.Column(db.String(17), nullable=True)

    observacoes = db.Column(db.Text, nullable=True)

    ativo = db.Column(db.Boolean, nullable=False, default=True)

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    atualizado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    cliente = db.relationship(
        "Cliente",
        backref=db.backref(
            "veiculos",
            lazy="select",
        ),
    )

    modelo = db.relationship(
        "Modelo",
        backref=db.backref(
            "veiculos",
            lazy="select",
        ),
    )

    porte = db.relationship(
        "PorteVeiculo",
        backref=db.backref(
            "veiculos",
            lazy="select",
        ),
    )

    ordens_servico = db.relationship(
        "OrdemServico",
        back_populates="veiculo",
    )

    def __repr__(self) -> str:
        return f"<Veiculo {self.id} - {self.placa}>"
