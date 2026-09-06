from unittest.mock import patch

from app.models.cliente import Cliente
from app.services.cliente_service import ClienteService


def test_criar_cliente_delega_para_repository():
    dados = {
        "tipo_pessoa": "PF",
        "nome_razao_social": "Cliente Teste",
        "nome_fantasia": "Teste",
        "cpf_cnpj": "12345678901",
        "email": "cliente@teste.com",
        "telefone": "(48) 99999-9999",
        "cidade": "Florianópolis",
        "uf": "SC",
    }

    with patch(
        "app.services.cliente_service.ClienteRepository.salvar"
    ) as mock_salvar:
        mock_salvar.side_effect = lambda cliente: cliente

        resultado = ClienteService.criar(dados)

        mock_salvar.assert_called_once()

        cliente = mock_salvar.call_args.args[0]

        assert isinstance(cliente, Cliente)
        assert cliente.tipo_pessoa == "PF"
        assert cliente.nome_razao_social == "Cliente Teste"
        assert cliente.nome_fantasia == "Teste"
        assert cliente.cpf_cnpj == "12345678901"
        assert cliente.email == "cliente@teste.com"
        assert cliente.telefone == "(48) 99999-9999"
        assert cliente.cidade == "Florianópolis"
        assert cliente.uf == "SC"

        assert resultado is cliente


def test_criar_cliente_aplica_campos_opcionais_como_none():
    dados = {
        "tipo_pessoa": "PJ",
        "nome_razao_social": "Empresa Teste",
        "email": "empresa@teste.com",
        "telefone": "(48) 3333-3333",
    }

    with patch(
        "app.services.cliente_service.ClienteRepository.salvar"
    ) as mock_salvar:
        mock_salvar.side_effect = lambda cliente: cliente

        resultado = ClienteService.criar(dados)

        cliente = mock_salvar.call_args.args[0]

        assert isinstance(cliente, Cliente)
        assert cliente.tipo_pessoa == "PJ"
        assert cliente.nome_razao_social == "Empresa Teste"
        assert cliente.nome_fantasia is None
        assert cliente.cpf_cnpj is None
        assert cliente.data_nascimento is None
        assert cliente.inscricao_estadual is None
        assert cliente.cep is None
        assert cliente.logradouro is None
        assert cliente.numero is None
        assert cliente.complemento is None
        assert cliente.bairro is None
        assert cliente.cidade is None
        assert cliente.uf is None

        assert resultado is cliente


def test_buscar_cliente_por_id_delega_para_repository():
    cliente = Cliente(
        id=123,
        tipo_pessoa="PF",
        nome_razao_social="Cliente Busca",
        email="busca@teste.com",
        telefone="48999999999",
    )

    with patch(
        "app.services.cliente_service.ClienteRepository.buscar_por_id",
        return_value=cliente,
    ) as mock_buscar:
        resultado = ClienteService.buscar_por_id(123)

        mock_buscar.assert_called_once_with(123)
        assert resultado is cliente


def test_buscar_cliente_por_cpf_cnpj_delega_para_repository():
    cliente = Cliente(
        id=123,
        tipo_pessoa="PF",
        nome_razao_social="Cliente CPF",
        cpf_cnpj="12345678901",
        email="cpf@teste.com",
        telefone="48999999999",
    )

    with patch(
        "app.services.cliente_service.ClienteRepository.buscar_por_cpf_cnpj",
        return_value=cliente,
    ) as mock_buscar:
        resultado = ClienteService.buscar_por_cpf_cnpj(
            "12345678901"
        )

        mock_buscar.assert_called_once_with(
            "12345678901"
        )
        assert resultado is cliente


def test_listar_todos_clientes_delega_para_repository():
    clientes = [
        Cliente(
            id=1,
            tipo_pessoa="PF",
            nome_razao_social="Cliente 1",
            email="cliente1@teste.com",
            telefone="48999999991",
        ),
        Cliente(
            id=2,
            tipo_pessoa="PJ",
            nome_razao_social="Cliente 2",
            email="cliente2@teste.com",
            telefone="48999999992",
        ),
    ]

    with patch(
        "app.services.cliente_service.ClienteRepository.listar_todos",
        return_value=clientes,
    ) as mock_listar:
        resultado = ClienteService.listar_todos()

        mock_listar.assert_called_once_with()
        assert resultado is clientes


def test_listar_clientes_ativos_delega_para_repository():
    clientes = [
        Cliente(
            id=1,
            tipo_pessoa="PF",
            nome_razao_social="Cliente Ativo",
            email="ativo@teste.com",
            telefone="48999999991",
        )
    ]

    with patch(
        "app.services.cliente_service.ClienteRepository.listar_ativos",
        return_value=clientes,
    ) as mock_listar:
        resultado = ClienteService.listar_ativos()

        mock_listar.assert_called_once_with()
        assert resultado is clientes


def test_excluir_cliente_delega_para_repository():
    cliente = Cliente(
        id=123,
        tipo_pessoa="PF",
        nome_razao_social="Cliente Excluir",
        email="excluir@teste.com",
        telefone="48999999999",
    )

    with patch(
        "app.services.cliente_service.ClienteRepository.excluir"
    ) as mock_excluir:
        resultado = ClienteService.excluir(cliente)

        mock_excluir.assert_called_once_with(cliente)
        assert resultado is None