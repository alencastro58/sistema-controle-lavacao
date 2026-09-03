from datetime import datetime, timezone

from app.extensions import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    tipo_pessoa = db.Column(db.String(2), nullable=False)
    nome_razao_social = db.Column(db.String(200), nullable=False)
    nome_fantasia = db.Column(db.String(200), nullable=True)

    cpf_cnpj = db.Column(db.String(14), unique=True, nullable=True)

    email = db.Column(db.String(254), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    data_nascimento = db.Column(db.Date, nullable=True)

    inscricao_estadual = db.Column(db.String(30), nullable=True)

    cep = db.Column(db.String(8), nullable=True)
    logradouro = db.Column(db.String(200), nullable=True)
    numero = db.Column(db.String(20), nullable=True)
    complemento = db.Column(db.String(100), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    uf = db.Column(db.String(2), nullable=True)

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

    ordens_servico = db.relationship(
        "OrdemServico",
        back_populates="cliente",
    )

    def __repr__(self) -> str:
        return f"<Cliente {self.id} - {self.nome_razao_social}>"
