"""adiciona controle de pagamento e entrega na ordem de servico

Revision ID: 51bf4c2d087b
Revises: 318deaa7964a
Create Date: 2026-09-04 19:27:45.671487

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "51bf4c2d087b"
down_revision: Union[str, Sequence[str], None] = "318deaa7964a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "ordens_servico",
        sa.Column(
            "pagamento_confirmado",
            sa.Boolean(),
            nullable=True,
        ),
    )

    op.add_column(
        "ordens_servico",
        sa.Column(
            "pagamento_confirmado_em",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.add_column(
        "ordens_servico",
        sa.Column(
            "veiculo_entregue",
            sa.Boolean(),
            nullable=True,
        ),
    )

    op.add_column(
        "ordens_servico",
        sa.Column(
            "veiculo_entregue_em",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.execute(
        sa.text(
            """
            UPDATE ordens_servico
            SET pagamento_confirmado = FALSE
            WHERE pagamento_confirmado IS NULL
            """
        )
    )

    op.execute(
        sa.text(
            """
            UPDATE ordens_servico
            SET veiculo_entregue = FALSE
            WHERE veiculo_entregue IS NULL
            """
        )
    )

    op.alter_column(
        "ordens_servico",
        "pagamento_confirmado",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=sa.false(),
    )

    op.alter_column(
        "ordens_servico",
        "veiculo_entregue",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=sa.false(),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("ordens_servico", "veiculo_entregue_em")
    op.drop_column("ordens_servico", "veiculo_entregue")
    op.drop_column("ordens_servico", "pagamento_confirmado_em")
    op.drop_column("ordens_servico", "pagamento_confirmado")
