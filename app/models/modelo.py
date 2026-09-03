from datetime import datetime, timezone

from app.extensions import db


class Modelo(db.Model):
    __tablename__ = "modelos"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    marca_id = db.Column(
        db.BigInteger,
        db.ForeignKey("marcas.id", ondelete="RESTRICT"),
        nullable=False,
    )

    nome = db.Column(db.String(100), nullable=False)

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

    marca = db.relationship(
        "Marca",
        backref=db.backref(
            "modelos",
            lazy="select",
        ),
    )

    __table_args__ = (
        db.UniqueConstraint(
            "marca_id",
            "nome",
            name="uq_modelos_marca_nome",
        ),
    )

    def __repr__(self) -> str:
        return f"<Modelo {self.id} - {self.nome}>"
