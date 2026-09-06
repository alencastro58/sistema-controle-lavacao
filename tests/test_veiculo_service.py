from app.models.cliente import Cliente
from app.models.marca import Marca
from app.models.modelo import Modelo
from app.models.porte_veiculo import PorteVeiculo
from app.models.veiculo import Veiculo
from app.services.veiculo_service import VeiculoService


def criar_dados_base():
    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social="Cliente Serviço",
        email="cliente.servico@example.com",
        telefone="48999990000",
    )

    marca = Marca(nome="Marca Serviço")

    porte = PorteVeiculo(
        nome="Porte Serviço",
        ordem=1,
    )

    from app.extensions import db

    db.session.add_all(
        [
            cliente,
            marca,
            porte,
        ]
    )
    db.session.flush()

    modelo = Modelo(
        marca_id=marca.id,
        nome="Modelo Serviço",
    )

    db.session.add(modelo)
    db.session.flush()

    return cliente, modelo, porte


def criar_dados_veiculo():
    cliente, modelo, porte = criar_dados_base()

    veiculo = VeiculoService.criar(
        {
            "cliente_id": cliente.id,
            "modelo_id": modelo.id,
            "porte_id": porte.id,
            "placa": "ABC1D23",
            "cor": "Preto",
            "ano_fabricacao": 2022,
            "ano_modelo": 2023,
            "renavam": "12345678901",
            "chassi": "9BWZZZ377VT004251",
            "observacoes": "Veículo de teste",
        }
    )

    return cliente, modelo, porte, veiculo


def test_criar_veiculo(app):
    with app.app_context():
        cliente, modelo, porte, veiculo = criar_dados_veiculo()

        assert veiculo.id is not None
        assert veiculo.cliente_id == cliente.id
        assert veiculo.modelo_id == modelo.id
        assert veiculo.porte_id == porte.id
        assert veiculo.placa == "ABC1D23"
        assert veiculo.cor == "Preto"
        assert veiculo.ano_fabricacao == 2022
        assert veiculo.ano_modelo == 2023


def test_buscar_veiculo_por_id(app):
    with app.app_context():
        _, _, _, veiculo = criar_dados_veiculo()

        resultado = VeiculoService.buscar_por_id(veiculo.id)

        assert resultado is not None
        assert resultado.id == veiculo.id
        assert resultado.placa == "ABC1D23"


def test_buscar_veiculo_por_placa(app):
    with app.app_context():
        _, _, _, veiculo = criar_dados_veiculo()

        resultado = VeiculoService.buscar_por_placa("ABC1D23")

        assert resultado is not None
        assert resultado.id == veiculo.id


def test_listar_todos_veiculos(app):
    with app.app_context():
        _, _, _, veiculo = criar_dados_veiculo()

        resultado = VeiculoService.listar_todos()

        ids = {item.id for item in resultado}

        assert veiculo.id in ids


def test_listar_veiculos_ativos(app):
    with app.app_context():
        _, _, _, veiculo = criar_dados_veiculo()

        resultado = VeiculoService.listar_ativos()

        ids = {item.id for item in resultado}

        assert veiculo.id in ids


def test_listar_veiculos_por_cliente(app):
    with app.app_context():
        cliente, _, _, veiculo = criar_dados_veiculo()

        resultado = VeiculoService.listar_por_cliente(cliente.id)

        ids = {item.id for item in resultado}

        assert veiculo.id in ids


def test_excluir_veiculo(app):
    with app.app_context():
        _, _, _, veiculo = criar_dados_veiculo()

        VeiculoService.excluir(veiculo)

        resultado = VeiculoService.buscar_por_id(veiculo.id)

        assert resultado is None