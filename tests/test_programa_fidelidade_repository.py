import pytest

from app.extensions import db
from app.models.programa_fidelidade import ProgramaFidelidade
from app.repositories.programa_fidelidade_repository import (
    ProgramaFidelidadeRepository,
)


@pytest.fixture
def programas_fidelidade_dados(app_context):
    programa_1 = ProgramaFidelidade(
        habilitado=False,
        pontos_por_real=1,
        valor_por_ponto=1,
        desconto_maximo_percentual=100,
    )

    programa_2 = ProgramaFidelidade(
        habilitado=True,
        pontos_por_real=1,
        valor_por_ponto=1,
        desconto_maximo_percentual=100,
    )

    db.session.add_all(
        [
            programa_1,
            programa_2,
        ]
    )
    db.session.commit()

    dados = {
        "programa_1_id": programa_1.id,
        "programa_2_id": programa_2.id,
    }

    yield dados

    db.session.rollback()

    for programa_id in [
        dados["programa_1_id"],
        dados["programa_2_id"],
    ]:
        programa = db.session.get(
            ProgramaFidelidade,
            programa_id,
        )

        if programa is not None:
            db.session.delete(programa)

    db.session.commit()


@pytest.mark.usefixtures("app_context")
def test_salvar_programa_fidelidade():
    programa = ProgramaFidelidade(
        habilitado=False,
        pontos_por_real=1,
        valor_por_ponto=1,
        desconto_maximo_percentual=100,
    )

    resultado = ProgramaFidelidadeRepository.salvar(programa)

    assert resultado is programa
    assert programa.id is not None

    db.session.delete(programa)
    db.session.commit()


@pytest.mark.usefixtures("app_context")
def test_buscar_programa_fidelidade_por_id(programas_fidelidade_dados):
    resultado = ProgramaFidelidadeRepository.buscar_por_id(
        programas_fidelidade_dados["programa_1_id"]
    )

    assert resultado is not None
    assert resultado.id == programas_fidelidade_dados["programa_1_id"]


@pytest.mark.usefixtures("app_context")
def test_buscar_programa_fidelidade_por_id_retorna_none_quando_nao_encontrado():
    resultado = ProgramaFidelidadeRepository.buscar_por_id(999999)

    assert resultado is None


@pytest.mark.usefixtures("app_context")
def test_buscar_primeiro_programa_fidelidade(programas_fidelidade_dados):
    resultado = ProgramaFidelidadeRepository.buscar_primeiro()

    assert resultado is not None
    assert resultado.id == programas_fidelidade_dados["programa_1_id"]


@pytest.mark.usefixtures("app_context")
def test_listar_programas_fidelidade(programas_fidelidade_dados):
    lista = ProgramaFidelidadeRepository.listar_todos()

    ids = {programa.id for programa in lista}

    assert programas_fidelidade_dados["programa_1_id"] in ids
    assert programas_fidelidade_dados["programa_2_id"] in ids