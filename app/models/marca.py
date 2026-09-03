from datetime import datetime, timezone

from app.extensions import db


class Marca(db.Model):
    __tablename__ = "marcas"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

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

    __table_args__ = (
        db.UniqueConstraint(
            "nome",
            name="uq_marcas_nome",
        ),
    )

    def __repr__(self) -> str:
        return f"<Marca {self.id} - {self.nome}>"
