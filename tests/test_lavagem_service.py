import pytest

from app.models.lavagem import Lavagem
from app.services.lavagem_service import LavagemService


@pytest.mark.usefixtures("app_context")
def test_iniciar_lavagem():
    lavagem = Lavagem(
        ordem_servico_id=1,
        status=LavagemService.STATUS_AGUARDANDO,
    )

    LavagemService.iniciar(lavagem)

    assert lavagem.status == LavagemService.STATUS_EM_ANDAMENTO
    assert lavagem.inicio is not None


@pytest.mark.usefixtures("app_context")
def test_concluir_lavagem():
    lavagem = Lavagem(
        ordem_servico_id=1,
        status=LavagemService.STATUS_EM_ANDAMENTO,
    )

    LavagemService.concluir(lavagem)

    assert lavagem.status == LavagemService.STATUS_CONCLUIDA
    assert lavagem.fim is not None


@pytest.mark.usefixtures("app_context")
def test_cancelar_lavagem_aguardando():
    lavagem = Lavagem(
        ordem_servico_id=1,
        status=LavagemService.STATUS_AGUARDANDO,
    )

    LavagemService.cancelar(lavagem)

    assert lavagem.status == LavagemService.STATUS_CANCELADA


@pytest.mark.usefixtures("app_context")
def test_cancelar_lavagem_em_andamento():
    lavagem = Lavagem(
        ordem_servico_id=1,
        status=LavagemService.STATUS_EM_ANDAMENTO,
    )

    LavagemService.cancelar(lavagem)

    assert lavagem.status == LavagemService.STATUS_CANCELADA


@pytest.mark.usefixtures("app_context")
def test_nao_permite_concluir_lavagem_aguardando():
    lavagem = Lavagem(
        ordem_servico_id=1,
        status=LavagemService.STATUS_AGUARDANDO,
    )

    try:
        LavagemService.concluir(lavagem)
        assert False, "A transição deveria ser rejeitada."
    except ValueError as exc:
        assert "AGUARDANDO -> CONCLUIDA" in str(exc)


@pytest.mark.usefixtures("app_context")
def test_nao_permite_reabrir_lavagem_concluida():
    lavagem = Lavagem(
        ordem_servico_id=1,
        status=LavagemService.STATUS_CONCLUIDA,
    )

    try:
        LavagemService.iniciar(lavagem)
        assert False, "A transição deveria ser rejeitada."
    except ValueError as exc:
        assert "CONCLUIDA -> EM_ANDAMENTO" in str(exc)


@pytest.mark.usefixtures("app_context")
def test_nao_permite_alterar_lavagem_cancelada():
    lavagem = Lavagem(
        ordem_servico_id=1,
        status=LavagemService.STATUS_CANCELADA,
    )

    try:
        LavagemService.iniciar(lavagem)
        assert False, "A transição deveria ser rejeitada."
    except ValueError as exc:
        assert "CANCELADA -> EM_ANDAMENTO" in str(exc)
