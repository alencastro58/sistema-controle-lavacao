from unittest.mock import patch

from app.models.programa_fidelidade import ProgramaFidelidade
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