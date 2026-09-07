"""cria estrutura do programa de fidelidade

Revision ID: 3bc342972b10
Revises: 51bf4c2d087b
Create Date: 2026-09-07 01:30:33.556292

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3bc342972b10"
down_revision: Union[str, Sequence[str], None] = "51bf4c2d087b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "programas_fidelidade",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("habilitado", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("versao_configuracao", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("criado_em", sa.DateTime(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "configuracoes_fidelidade",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("programa_id", sa.BigInteger(), nullable=False),
        sa.Column("evento_geracao", sa.String(length=30), nullable=False),
        sa.Column("base_calculo_padrao", sa.String(length=30), nullable=False),
        sa.Column("tipo_pontos_padrao", sa.String(length=20), nullable=False),
        sa.Column("arredondamento_padrao", sa.String(length=20), nullable=False),
        sa.Column("validade_tipo_padrao", sa.String(length=20), nullable=False),
        sa.Column("validade_dias_padrao", sa.Integer(), nullable=True),
        sa.Column("validade_data_padrao", sa.DateTime(), nullable=True),
        sa.Column("permite_desconto_monetario", sa.Boolean(), nullable=False),
        sa.Column("permite_beneficios", sa.Boolean(), nullable=False),
        sa.Column("permite_os_geradora", sa.Boolean(), nullable=False),
        sa.Column("permite_pagamento_integral", sa.Boolean(), nullable=False),
        sa.Column("limite_percentual_os", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("limite_monetario_os", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("politica_estorno", sa.String(length=30), nullable=False),
        sa.Column("politica_expiracao", sa.String(length=30), nullable=False),
        sa.Column("criado_em", sa.DateTime(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["programa_id"],
            ["programas_fidelidade.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "programa_id",
            name="uq_configuracoes_fidelidade_programa",
        ),
    )

    op.create_table(
        "regras_fidelidade",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("programa_id", sa.BigInteger(), nullable=False),
        sa.Column("servico_id", sa.BigInteger(), nullable=True),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("tipo_regra", sa.String(length=30), nullable=False),
        sa.Column("prioridade", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("base_calculo", sa.String(length=30), nullable=False),
        sa.Column("tipo_pontos", sa.String(length=20), nullable=False),
        sa.Column("arredondamento", sa.String(length=20), nullable=False),
        sa.Column("pontos_fixos", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("valor_por_ponto", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("pontos_por_valor", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("valor_minimo", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("valor_maximo", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("validade_tipo", sa.String(length=20), nullable=False),
        sa.Column("validade_dias", sa.Integer(), nullable=True),
        sa.Column("validade_data", sa.DateTime(), nullable=True),
        sa.Column("criado_em", sa.DateTime(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["programa_id"],
            ["programas_fidelidade.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["servico_id"],
            ["servicos.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "beneficios_fidelidade",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("programa_id", sa.BigInteger(), nullable=False),
        sa.Column("nome", sa.String(length=120), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("custo_pontos", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("valor_monetario", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("servico_id", sa.BigInteger(), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("validade_tipo", sa.String(length=20), nullable=False),
        sa.Column("validade_dias", sa.Integer(), nullable=True),
        sa.Column("validade_data", sa.DateTime(), nullable=True),
        sa.Column("prazo_utilizacao_tipo", sa.String(length=20), nullable=False),
        sa.Column("prazo_utilizacao_dias", sa.Integer(), nullable=True),
        sa.Column("permite_pagamento_integral", sa.Boolean(), nullable=False),
        sa.Column("politica_debito", sa.String(length=30), nullable=False),
        sa.Column("politica_expiracao", sa.String(length=30), nullable=False),
        sa.Column("criado_em", sa.DateTime(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["programa_id"],
            ["programas_fidelidade.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["servico_id"],
            ["servicos.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "saldos_fidelidade",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("programa_id", sa.BigInteger(), nullable=False),
        sa.Column("cliente_id", sa.BigInteger(), nullable=False),
        sa.Column("saldo_pontos", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("criado_em", sa.DateTime(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["programa_id"],
            ["programas_fidelidade.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["cliente_id"],
            ["clientes.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "programa_id",
            "cliente_id",
            name="uq_saldos_fidelidade_programa_cliente",
        ),
    )

    op.create_table(
        "movimentacoes_fidelidade",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("programa_id", sa.BigInteger(), nullable=False),
        sa.Column("cliente_id", sa.BigInteger(), nullable=False),
        sa.Column("saldo_id", sa.BigInteger(), nullable=False),
        sa.Column("ordem_servico_id", sa.BigInteger(), nullable=True),
        sa.Column("tipo", sa.String(length=30), nullable=False),
        sa.Column("pontos", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("saldo_anterior", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("saldo_posterior", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("regra_id", sa.BigInteger(), nullable=True),
        sa.Column("beneficio_id", sa.BigInteger(), nullable=True),
        sa.Column("versao_configuracao", sa.Integer(), nullable=False),
        sa.Column("base_calculo", sa.String(length=30), nullable=True),
        sa.Column("valor_base", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("conversao_pontos", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("validade_em", sa.DateTime(), nullable=True),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("criado_em", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["programa_id"],
            ["programas_fidelidade.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["cliente_id"],
            ["clientes.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["saldo_id"],
            ["saldos_fidelidade.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["ordem_servico_id"],
            ["ordens_servico.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["regra_id"],
            ["regras_fidelidade.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["beneficio_id"],
            ["beneficios_fidelidade.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "resgates_fidelidade",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("programa_id", sa.BigInteger(), nullable=False),
        sa.Column("cliente_id", sa.BigInteger(), nullable=False),
        sa.Column("saldo_id", sa.BigInteger(), nullable=False),
        sa.Column("ordem_servico_id", sa.BigInteger(), nullable=True),
        sa.Column("beneficio_id", sa.BigInteger(), nullable=True),
        sa.Column("modalidade", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("pontos_solicitados", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("pontos_debitados", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("valor_desconto", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("conversao_pontos", sa.Numeric(precision=12, scale=4), nullable=True),
        sa.Column("data_solicitacao", sa.DateTime(), nullable=False),
        sa.Column("data_aprovacao", sa.DateTime(), nullable=True),
        sa.Column("data_utilizacao", sa.DateTime(), nullable=True),
        sa.Column("data_cancelamento", sa.DateTime(), nullable=True),
        sa.Column("data_expiracao", sa.DateTime(), nullable=True),
        sa.Column("versao_configuracao", sa.Integer(), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("criado_em", sa.DateTime(), nullable=False),
        sa.Column("atualizado_em", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["programa_id"],
            ["programas_fidelidade.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["cliente_id"],
            ["clientes.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["saldo_id"],
            ["saldos_fidelidade.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["ordem_servico_id"],
            ["ordens_servico.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["beneficio_id"],
            ["beneficios_fidelidade.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("resgates_fidelidade")
    op.drop_table("movimentacoes_fidelidade")
    op.drop_table("saldos_fidelidade")
    op.drop_table("beneficios_fidelidade")
    op.drop_table("regras_fidelidade")
    op.drop_table("configuracoes_fidelidade")
    op.drop_table("programas_fidelidade")