from unittest.mock import patch

from app.models.preco_servico import PrecoServico
from app.services.preco_servico_service import PrecoServicoService


def test_criar_preco_servico_delega_para_repository():
    dados = {
        "servico_id": 10,
        "porte_id": 20,
        "valor": 50.00,
        "ativo": True,
    }

    with patch(
        "app.services.preco_servico_service.PrecoServicoRepository.salvar"
    ) as mock_salvar:
        mock_salvar.side_effect = lambda preco: preco

        resultado = PrecoServicoService.criar(dados)

        mock_salvar.assert_called_once()

        preco_servico = mock_salvar.call_args.args[0]

        assert isinstance(preco_servico, PrecoServico)
        assert preco_servico.servico_id == 10
        assert preco_servico.porte_id == 20
        assert preco_servico.valor == 50.00
        assert preco_servico.ativo is True

        assert resultado is preco_servico


def test_criar_preco_servico_aplica_ativo_por_padrao():
    dados = {
        "servico_id": 10,
        "porte_id": 20,
        "valor": 50.00,
    }

    with patch(
        "app.services.preco_servico_service.PrecoServicoRepository.salvar"
    ) as mock_salvar:
        mock_salvar.side_effect = lambda preco: preco

        resultado = PrecoServicoService.criar(dados)

        mock_salvar.assert_called_once()

        preco_servico = mock_salvar.call_args.args[0]

        assert isinstance(preco_servico, PrecoServico)
        assert preco_servico.servico_id == 10
        assert preco_servico.porte_id == 20
        assert preco_servico.valor == 50.00
        assert preco_servico.ativo is True

        assert resultado is preco_servico


def test_buscar_preco_servico_por_id_delega_para_repository():
    preco_servico = PrecoServico(
        id=123,
        servico_id=10,
        porte_id=20,
        valor=50.00,
        ativo=True,
    )

    with patch(
        "app.services.preco_servico_service.PrecoServicoRepository.buscar_por_id",
        return_value=preco_servico,
    ) as mock_buscar:

        resultado = PrecoServicoService.buscar_por_id(123)

        mock_buscar.assert_called_once_with(123)

        assert resultado is preco_servico


def test_listar_todos_precos_servicos_delega_para_repository():
    precos = [
        PrecoServico(
            id=1,
            servico_id=10,
            porte_id=20,
            valor=40.00,
            ativo=True,
        ),
        PrecoServico(
            id=2,
            servico_id=10,
            porte_id=21,
            valor=50.00,
            ativo=True,
        ),
    ]

    with patch(
        "app.services.preco_servico_service.PrecoServicoRepository.listar_todos",
        return_value=precos,
    ) as mock_listar:

        resultado = PrecoServicoService.listar_todos()

        mock_listar.assert_called_once_with()

        assert resultado is precos


def test_listar_precos_por_servico_delega_para_repository():
    precos = [
        PrecoServico(
            id=1,
            servico_id=10,
            porte_id=20,
            valor=40.00,
            ativo=True,
        ),
        PrecoServico(
            id=2,
            servico_id=10,
            porte_id=21,
            valor=50.00,
            ativo=True,
        ),
    ]

    with patch(
        "app.services.preco_servico_service.PrecoServicoRepository.listar_por_servico",
        return_value=precos,
    ) as mock_listar:

        resultado = PrecoServicoService.listar_por_servico(10)

        mock_listar.assert_called_once_with(10)

        assert resultado is precos


def test_listar_precos_por_porte_delega_para_repository():
    precos = [
        PrecoServico(
            id=1,
            servico_id=10,
            porte_id=20,
            valor=40.00,
            ativo=True,
        ),
        PrecoServico(
            id=2,
            servico_id=11,
            porte_id=20,
            valor=60.00,
            ativo=True,
        ),
    ]

    with patch(
        "app.services.preco_servico_service.PrecoServicoRepository.listar_por_porte",
        return_value=precos,
    ) as mock_listar:

        resultado = PrecoServicoService.listar_por_porte(20)

        mock_listar.assert_called_once_with(20)

        assert resultado is precos


def test_excluir_preco_servico_delega_para_repository():
    preco_servico = PrecoServico(
        id=123,
        servico_id=10,
        porte_id=20,
        valor=50.00,
        ativo=True,
    )

    with patch(
        "app.services.preco_servico_service.PrecoServicoRepository.excluir"
    ) as mock_excluir:

        resultado = PrecoServicoService.excluir(
            preco_servico
        )

        mock_excluir.assert_called_once_with(
            preco_servico
        )

        assert resultado is None
