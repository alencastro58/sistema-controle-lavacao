from decimal import Decimal
from unittest.mock import patch

import pytest

from app.models.movimentacao_fidelidade import MovimentacaoFidelidade
from app.models.ordem_servico import OrdemServico
from app.models.programa_fidelidade import ProgramaFidelidade
from app.models.saldo_fidelidade import SaldoFidelidade
from app.services.programa_fidelidade_service import (
    ProgramaFidelidadeService,
)


def test_criar_programa_fidelidade_delega_para_repository():
    dados = {
        "habilitado": False,
        "pontos_por_real": 1,
        "valor_por_ponto": 1,
        "desconto_maximo_percentual": 100,
    }

    with patch(
        "app.services.programa_fidelidade_service.ProgramaFidelidadeRepository.salvar"
    ) as mock_salvar:
        mock_salvar.side_effect = lambda programa: programa

        resultado = ProgramaFidelidadeService.criar(dados)

        mock_salvar.assert_called_once()

        programa = mock_salvar.call_args.args[0]

        assert isinstance(programa, ProgramaFidelidade)
        assert programa.habilitado is False
        assert programa.pontos_por_real == 1
        assert programa.valor_por_ponto == 1
        assert programa.desconto_maximo_percentual == 100

        assert resultado is programa


def test_criar_programa_fidelidade_aplica_campos_opcionais():
    dados = {}

    with patch(
        "app.services.programa_fidelidade_service.ProgramaFidelidadeRepository.salvar"
    ) as mock_salvar:
        mock_salvar.side_effect = lambda programa: programa

        resultado = ProgramaFidelidadeService.criar(dados)

        mock_salvar.assert_called_once()

        programa = mock_salvar.call_args.args[0]

        assert isinstance(programa, ProgramaFidelidade)
        assert programa.habilitado is False
        assert programa.pontos_por_real == 1
        assert programa.valor_por_ponto == 1
        assert programa.desconto_maximo_percentual == 100

        assert resultado is programa


def test_buscar_programa_fidelidade_por_id_delega_para_repository():
    programa = ProgramaFidelidade(
        id=123,
        habilitado=False,
        pontos_por_real=1,
        valor_por_ponto=1,
        desconto_maximo_percentual=100,
    )

    with patch(
        "app.services.programa_fidelidade_service.ProgramaFidelidadeRepository.buscar_por_id",
        return_value=programa,
    ) as mock_buscar:
        resultado = ProgramaFidelidadeService.buscar_por_id(123)

        mock_buscar.assert_called_once_with(123)
        assert resultado is programa


def test_buscar_primeiro_programa_fidelidade_delega_para_repository():
    programa = ProgramaFidelidade(
        id=123,
        habilitado=False,
        pontos_por_real=1,
        valor_por_ponto=1,
        desconto_maximo_percentual=100,
    )

    with patch(
        "app.services.programa_fidelidade_service.ProgramaFidelidadeRepository.buscar_primeiro",
        return_value=programa,
    ) as mock_buscar:
        resultado = ProgramaFidelidadeService.buscar_primeiro()

        mock_buscar.assert_called_once_with()
        assert resultado is programa


def test_listar_programas_fidelidade_delega_para_repository():
    programas = [
        ProgramaFidelidade(
            id=1,
            habilitado=False,
            pontos_por_real=1,
            valor_por_ponto=1,
            desconto_maximo_percentual=100,
        ),
        ProgramaFidelidade(
            id=2,
            habilitado=False,
            pontos_por_real=1,
            valor_por_ponto=1,
            desconto_maximo_percentual=100,
        ),
    ]

    with patch(
        "app.services.programa_fidelidade_service.ProgramaFidelidadeRepository.listar_todos",
        return_value=programas,
    ) as mock_listar:
        resultado = ProgramaFidelidadeService.listar_todos()

        mock_listar.assert_called_once_with()
        assert resultado is programas


def criar_programa():
    return ProgramaFidelidade(
        id=1,
        habilitado=True,
        pontos_por_real=1,
        valor_por_ponto=1,
        desconto_maximo_percentual=100,
    )


def criar_ordem():
    return OrdemServico(
        id=10,
        numero="OS-FIDELIDADE-001",
        cliente_id=20,
        veiculo_id=30,
        valor_total=100,
        desconto=0,
    )


def criar_saldo():
    return SaldoFidelidade(
        id=2,
        programa_id=1,
        cliente_id=20,
        saldo_pontos=50,
        total_acumulado=50,
        total_utilizado=0,
    )


def configurar_debito(programa=None, saldo=None, movimentacoes=None):
    programa = programa or criar_programa()
    saldo = saldo or criar_saldo()
    movimentacoes = movimentacoes or []

    patches = [
        patch(
            "app.services.programa_fidelidade_service.ProgramaFidelidadeRepository.buscar_primeiro",
            return_value=programa,
        ),
        patch(
            "app.services.programa_fidelidade_service.MovimentacaoFidelidadeRepository.buscar_por_ordem_servico",
            return_value=movimentacoes,
        ),
        patch(
            "app.services.programa_fidelidade_service.SaldoFidelidadeRepository.buscar_por_programa_e_cliente",
            return_value=saldo,
        ),
        patch(
            "app.services.programa_fidelidade_service.MovimentacaoFidelidadeRepository.salvar",
            side_effect=lambda movimentacao: movimentacao,
        ),
    ]

    return patches


def test_debitar_pontos_recebe_desconto_em_reais_e_calcula_pontos():
    programa = criar_programa()
    saldo = criar_saldo()
    ordem = criar_ordem()

    patches = configurar_debito(programa, saldo)

    with patches[0], patches[1], patches[2], patches[3]:
        resultado = ProgramaFidelidadeService.debitar_pontos(
            cliente_id=20,
            valor_desconto=Decimal("30.00"),
            ordem_servico=ordem,
        )

    assert isinstance(resultado, MovimentacaoFidelidade)
    assert resultado.tipo == "DEBITO"
    assert resultado.pontos == Decimal("30")
    assert resultado.valor_base == Decimal("30.00")
    assert resultado.conversao_pontos == Decimal("1")
    assert resultado.saldo_anterior == Decimal("50")
    assert resultado.saldo_posterior == Decimal("20")

    assert saldo.saldo_pontos == Decimal("20")
    assert saldo.total_utilizado == Decimal("30")
    assert ordem.desconto == Decimal("30.00")


def test_debitar_pontos_exige_desconto_multiplo_exato():
    programa = criar_programa()
    programa.valor_por_ponto = Decimal("3")
    saldo = criar_saldo()
    ordem = criar_ordem()

    patches = configurar_debito(programa, saldo)

    with patches[0], patches[1], patches[2], patches[3]:
        with pytest.raises(ValueError, match="múltiplo exato"):
            ProgramaFidelidadeService.debitar_pontos(
                cliente_id=20,
                valor_desconto=Decimal("10.00"),
                ordem_servico=ordem,
            )

    assert saldo.saldo_pontos == Decimal("50")
    assert ordem.desconto == Decimal("0")


def test_debitar_pontos_rejeita_saldo_insuficiente():
    programa = criar_programa()
    saldo = criar_saldo()
    saldo.saldo_pontos = 20
    ordem = criar_ordem()

    patches = configurar_debito(programa, saldo)

    with patches[0], patches[1], patches[2], patches[3]:
        with pytest.raises(ValueError, match="saldo de pontos suficiente"):
            ProgramaFidelidadeService.debitar_pontos(
                cliente_id=20,
                valor_desconto=Decimal("30.00"),
                ordem_servico=ordem,
            )

    assert saldo.saldo_pontos == Decimal("20")
    assert ordem.desconto == Decimal("0")


def test_debitar_pontos_rejeita_desconto_acima_do_limite():
    programa = criar_programa()
    programa.desconto_maximo_percentual = 20
    saldo = criar_saldo()
    ordem = criar_ordem()

    patches = configurar_debito(programa, saldo)

    with patches[0], patches[1], patches[2], patches[3]:
        with pytest.raises(ValueError, match="limite permitido"):
            ProgramaFidelidadeService.debitar_pontos(
                cliente_id=20,
                valor_desconto=Decimal("30.00"),
                ordem_servico=ordem,
            )

    assert saldo.saldo_pontos == Decimal("50")
    assert ordem.desconto == Decimal("0")


def test_debitar_pontos_rejeita_desconto_acima_do_valor_disponivel():
    programa = criar_programa()
    saldo = criar_saldo()
    ordem = criar_ordem()
    ordem.desconto = 80

    patches = configurar_debito(programa, saldo)

    with patches[0], patches[1], patches[2], patches[3]:
        with pytest.raises(ValueError, match="valor disponível"):
            ProgramaFidelidadeService.debitar_pontos(
                cliente_id=20,
                valor_desconto=Decimal("30.00"),
                ordem_servico=ordem,
            )

    assert saldo.saldo_pontos == Decimal("50")
    assert ordem.desconto == Decimal("80")


def test_debitar_pontos_rejeita_debito_duplicado_na_mesma_os():
    programa = criar_programa()
    saldo = criar_saldo()
    ordem = criar_ordem()

    movimentacao_existente = MovimentacaoFidelidade(
        id=99,
        programa_id=1,
        cliente_id=20,
        saldo_id=2,
        ordem_servico_id=10,
        tipo="DEBITO",
        pontos=10,
        saldo_anterior=60,
        saldo_posterior=50,
        valor_base=10,
        conversao_pontos=1,
    )

    patches = configurar_debito(
        programa,
        saldo,
        [movimentacao_existente],
    )

    with patches[0], patches[1], patches[2], patches[3]:
        with pytest.raises(ValueError, match="já utilizou pontos"):
            ProgramaFidelidadeService.debitar_pontos(
                cliente_id=20,
                valor_desconto=Decimal("30.00"),
                ordem_servico=ordem,
            )

    assert saldo.saldo_pontos == Decimal("50")
    assert ordem.desconto == Decimal("0")