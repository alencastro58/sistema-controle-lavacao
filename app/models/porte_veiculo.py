from datetime import datetime, timezone

from app.extensions import db


class PorteVeiculo(db.Model):
    __tablename__ = "portes_veiculo"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    nome = db.Column(db.String(50), nullable=False)

    ordem = db.Column(db.SmallInteger, nullable=False, default=0)

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
            name="uq_portes_veiculo_nome",
        ),
    )
    
    precos_servicos = db.relationship(
        "PrecoServico",
        back_populates="porte",
    )

    def __repr__(self) -> str:
        return f"<PorteVeiculo {self.id} - {self.nome}>"
