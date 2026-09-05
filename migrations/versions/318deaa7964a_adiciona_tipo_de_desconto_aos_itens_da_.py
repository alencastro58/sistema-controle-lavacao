"""adiciona tipo de desconto aos itens da ordem de servico

Revision ID: 318deaa7964a
Revises: 3c6c8887f97d
Create Date: 2026-09-03 19:23:19.131849

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "318deaa7964a"
down_revision: Union[str, Sequence[str], None] = "3c6c8887f97d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Adiciona o tipo de desconto aos itens existentes e novos."""

    op.add_column(
        "itens_ordem_servico",
        sa.Column(
            "tipo_desconto",
            sa.String(length=20),
            nullable=False,
            server_default="NENHUM",
        ),
    )


def downgrade() -> None:
    """Remove o tipo de desconto dos itens da ordem de serviço."""

    op.drop_column(
        "itens_ordem_servico",
        "tipo_desconto",
    )