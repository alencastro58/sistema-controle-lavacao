"""simplifica estrutura do programa de fidelidade

Revision ID: 7e530be8bbff
Revises: 3bc342972b10
Create Date: 2026-09-07

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7e530be8bbff"
down_revision: Union[str, Sequence[str], None] = "3bc342972b10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Simplifica a estrutura do programa de fidelidade."""

    # Remove primeiro as chaves estrangeiras que impedem
    # a exclusão das tabelas antigas.
    op.drop_constraint(
        "movimentacoes_fidelidade_beneficio_id_fkey",
        "movimentacoes_fidelidade",
        type_="foreignkey",
    )
    op.drop_constraint(
        "movimentacoes_fidelidade_regra_id_fkey",
        "movimentacoes_fidelidade",
        type_="foreignkey",
    )
    op.drop_constraint(
        "resgates_fidelidade_beneficio_id_fkey",
        "resgates_fidelidade",
        type_="foreignkey",
    )

    # Remove as tabelas que não fazem mais parte do modelo mínimo.
    op.drop_table("resgates_fidelidade")
    op.drop_table("beneficios_fidelidade")
    op.drop_table("regras_fidelidade")
    op.drop_table("configuracoes_fidelidade")

    # Simplifica o programa de fidelidade.
    op.drop_column("programas_fidelidade", "nome")
    op.drop_column("programas_fidelidade", "descricao")
    op.drop_column("programas_fidelidade", "versao_configuracao")

    op.add_column(
        "programas_fidelidade",
        sa.Column(
            "pontos_por_real",
            sa.Numeric(precision=12, scale=4),
            nullable=False,
            server_default="1",
        ),
    )
    op.add_column(
        "programas_fidelidade",
        sa.Column(
            "valor_por_ponto",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
            server_default="1",
        ),
    )
    op.add_column(
        "programas_fidelidade",
        sa.Column(
            "desconto_maximo_percentual",
            sa.Numeric(precision=5, scale=2),
            nullable=False,
            server_default="100",
        ),
    )

    # Adiciona os acumuladores ao saldo do cliente.
    op.add_column(
        "saldos_fidelidade",
        sa.Column(
            "total_acumulado",
            sa.Numeric(precision=12, scale=4),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "saldos_fidelidade",
        sa.Column(
            "total_utilizado",
            sa.Numeric(precision=12, scale=4),
            nullable=False,
            server_default="0",
        ),
    )

    # Remove referências às estruturas antigas.
    op.drop_column("movimentacoes_fidelidade", "regra_id")
    op.drop_column("movimentacoes_fidelidade", "beneficio_id")
    op.drop_column("movimentacoes_fidelidade", "versao_configuracao")
    op.drop_column("movimentacoes_fidelidade", "base_calculo")
    op.drop_column("movimentacoes_fidelidade", "validade_em")


def downgrade() -> None:
    """Reversão não implementada para a estrutura antiga."""

    raise NotImplementedError(
        "A reversão da simplificação da fidelidade não está implementada."
    )