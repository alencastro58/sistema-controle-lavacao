from unittest.mock import patch

from app.models.ordem_servico import OrdemServico
from app.services.ordem_servico_service import OrdemServicoService


def test_criar_ordem_servico_delega_para_repository():
    dados = {
        "numero": "OS-TESTE-001",
        "cliente_id": 10,
        "veiculo_id": 20,
        "valor_total": 150,
        "desconto": 10,
        "status": "ABERTA",
        "observacoes": "Teste de criação",
    }

    with patch(
        "app.services.ordem_servico_service.OrdemServicoRepository.salvar"
    ) as mock_salvar:
        mock_salvar.side_effect = lambda ordem: ordem

        resultado = OrdemServicoService.criar(dados)

        mock_salvar.assert_called_once()

        ordem_servico = mock_salvar.call_args.args[0]

        assert isinstance(ordem_servico, OrdemServico)
        assert ordem_servico.numero == "OS-TESTE-001"
        assert ordem_servico.cliente_id == 10
        assert ordem_servico.veiculo_id == 20
        assert ordem_servico.valor_total == 150
        assert ordem_servico.desconto == 10
        assert ordem_servico.status == "ABERTA"
        assert ordem_servico.observacoes == "Teste de criação"

        assert resultado is ordem_servico


def test_criar_ordem_servico_aplica_valores_padrao():
    dados = {
        "numero": "OS-TESTE-002",
        "cliente_id": 10,
        "veiculo_id": 20,
    }

    with patch(
        "app.services.ordem_servico_service.OrdemServicoRepository.salvar"
    ) as mock_salvar:
        mock_salvar.side_effect = lambda ordem: ordem

        resultado = OrdemServicoService.criar(dados)

        mock_salvar.assert_called_once()

        ordem_servico = mock_salvar.call_args.args[0]

        assert isinstance(ordem_servico, OrdemServico)
        assert ordem_servico.numero == "OS-TESTE-002"
        assert ordem_servico.cliente_id == 10
        assert ordem_servico.veiculo_id == 20
        assert ordem_servico.valor_total == 0
        assert ordem_servico.desconto == 0
        assert ordem_servico.status == "ABERTA"
        assert ordem_servico.observacoes is None

        assert resultado is ordem_servico


def test_buscar_ordem_servico_por_id_delega_para_repository():
    ordem_servico = OrdemServico(
        id=123,
        numero="OS-BUSCA-001",
        cliente_id=10,
        veiculo_id=20,
    )

    with patch(
        "app.services.ordem_servico_service.OrdemServicoRepository.buscar_por_id",
        return_value=ordem_servico,
    ) as mock_buscar:

        resultado = OrdemServicoService.buscar_por_id(123)

        mock_buscar.assert_called_once_with(123)

        assert resultado is ordem_servico


def test_listar_todas_ordens_servico_delega_para_repository():
    ordens_servico = [
        OrdemServico(
            id=1,
            numero="OS-LISTA-001",
            cliente_id=10,
            veiculo_id=20,
        ),
        OrdemServico(
            id=2,
            numero="OS-LISTA-002",
            cliente_id=11,
            veiculo_id=21,
        ),
    ]

    with patch(
        "app.services.ordem_servico_service.OrdemServicoRepository.listar_todas",
        return_value=ordens_servico,
    ) as mock_listar:

        resultado = OrdemServicoService.listar_todas()

        mock_listar.assert_called_once_with()

        assert resultado is ordens_servico


def test_listar_ordens_servico_por_cliente_delega_para_repository():
    ordens_servico = [
        OrdemServico(
            id=1,
            numero="OS-CLIENTE-001",
            cliente_id=10,
            veiculo_id=20,
        ),
        OrdemServico(
            id=2,
            numero="OS-CLIENTE-002",
            cliente_id=10,
            veiculo_id=21,
        ),
    ]

    with patch(
        "app.services.ordem_servico_service.OrdemServicoRepository.listar_por_cliente",
        return_value=ordens_servico,
    ) as mock_listar:

        resultado = OrdemServicoService.listar_por_cliente(10)

        mock_listar.assert_called_once_with(10)

        assert resultado is ordens_servico


def test_listar_ordens_servico_por_veiculo_delega_para_repository():
    ordens_servico = [
        OrdemServico(
            id=1,
            numero="OS-VEICULO-001",
            cliente_id=10,
            veiculo_id=20,
        ),
        OrdemServico(
            id=2,
            numero="OS-VEICULO-002",
            cliente_id=11,
            veiculo_id=20,
        ),
    ]

    with patch(
        "app.services.ordem_servico_service.OrdemServicoRepository.listar_por_veiculo",
        return_value=ordens_servico,
    ) as mock_listar:

        resultado = OrdemServicoService.listar_por_veiculo(20)

        mock_listar.assert_called_once_with(20)

        assert resultado is ordens_servico

def test_excluir_ordem_servico_delega_para_repository():
    ordem_servico = OrdemServico(
        id=123,
        numero="OS-EXCLUIR-001",
        cliente_id=10,
        veiculo_id=20,
    )

    with patch(
        "app.services.ordem_servico_service.OrdemServicoRepository.excluir"
    ) as mock_excluir:

        resultado = OrdemServicoService.excluir(
            ordem_servico
        )

        mock_excluir.assert_called_once_with(
            ordem_servico
        )

        assert resultado is None
