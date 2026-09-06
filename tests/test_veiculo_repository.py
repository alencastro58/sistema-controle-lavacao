from app.extensions import db
from app.models.cliente import Cliente
from app.models.marca import Marca
from app.models.modelo import Modelo
from app.models.porte_veiculo import PorteVeiculo
from app.models.veiculo import Veiculo
from app.repositories.veiculo_repository import VeiculoRepository


def criar_cliente(
    nome_razao_social: str = "Cliente Teste",
) -> Cliente:
    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=nome_razao_social,
        email="cliente.teste@example.com",
        telefone="48999999999",
        ativo=True,
    )

    db.session.add(cliente)
    db.session.flush()

    return cliente


def criar_marca(
    nome: str = "Marca Teste",
) -> Marca:
    marca = Marca(
        nome=nome,
        ativo=True,
    )

    db.session.add(marca)
    db.session.flush()

    return marca


def criar_modelo(
    marca: Marca,
    nome: str = "Modelo Teste",
) -> Modelo:
    modelo = Modelo(
        marca_id=marca.id,
        nome=nome,
        ativo=True,
    )

    db.session.add(modelo)
    db.session.flush()

    return modelo


def criar_porte(
    nome: str = "Porte Teste",
) -> PorteVeiculo:
    porte = PorteVeiculo(
        nome=nome,
        ordem=1,
        ativo=True,
    )

    db.session.add(porte)
    db.session.flush()

    return porte


def criar_veiculo(
    cliente: Cliente,
    modelo: Modelo,
    porte: PorteVeiculo,
    placa: str = "ABC1D23",
    cor: str = "Branco",
) -> Veiculo:
    return Veiculo(
        cliente_id=cliente.id,
        modelo_id=modelo.id,
        porte_id=porte.id,
        placa=placa,
        cor=cor,
        ativo=True,
    )


def preparar_dependencias():
    cliente = criar_cliente()
    marca = criar_marca()
    modelo = criar_modelo(marca)
    porte = criar_porte()

    return cliente, marca, modelo, porte


def test_salvar_e_buscar_veiculo_por_id(app):
    with app.app_context():
        cliente, _, modelo, porte = preparar_dependencias()

        veiculo = criar_veiculo(
            cliente=cliente,
            modelo=modelo,
            porte=porte,
        )

        resultado = VeiculoRepository.salvar(veiculo)

        assert resultado.id is not None
        assert resultado.placa == "ABC1D23"

        encontrado = VeiculoRepository.buscar_por_id(
            resultado.id
        )

        assert encontrado is not None
        assert encontrado.id == resultado.id
        assert encontrado.placa == "ABC1D23"
        assert encontrado.cliente_id == cliente.id
        assert encontrado.modelo_id == modelo.id
        assert encontrado.porte_id == porte.id


def test_buscar_veiculo_por_placa(app):
    with app.app_context():
        cliente, _, modelo, porte = preparar_dependencias()

        veiculo = criar_veiculo(
            cliente=cliente,
            modelo=modelo,
            porte=porte,
            placa="DEF4G56",
        )

        VeiculoRepository.salvar(veiculo)

        encontrado = VeiculoRepository.buscar_por_placa(
            "DEF4G56"
        )

        assert encontrado is not None
        assert encontrado.id == veiculo.id
        assert encontrado.placa == "DEF4G56"


def test_buscar_veiculo_por_placa_inexistente(app):
    with app.app_context():
        resultado = VeiculoRepository.buscar_por_placa(
            "ZZZ9Z99"
        )

        assert resultado is None


def test_listar_todos_os_veiculos(app):
    with app.app_context():
        cliente, _, modelo, porte = preparar_dependencias()

        primeiro = criar_veiculo(
            cliente=cliente,
            modelo=modelo,
            porte=porte,
            placa="AAA1A11",
        )

        segundo = criar_veiculo(
            cliente=cliente,
            modelo=modelo,
            porte=porte,
            placa="BBB2B22",
        )

        VeiculoRepository.salvar(primeiro)
        VeiculoRepository.salvar(segundo)

        veiculos = VeiculoRepository.listar_todos()

        placas = {veiculo.placa for veiculo in veiculos}

        assert "AAA1A11" in placas
        assert "BBB2B22" in placas


def test_listar_apenas_veiculos_ativos(app):
    with app.app_context():
        cliente, _, modelo, porte = preparar_dependencias()

        ativo = criar_veiculo(
            cliente=cliente,
            modelo=modelo,
            porte=porte,
            placa="CCC3C33",
        )

        inativo = criar_veiculo(
            cliente=cliente,
            modelo=modelo,
            porte=porte,
            placa="DDD4D44",
        )
        inativo.ativo = False

        VeiculoRepository.salvar(ativo)
        VeiculoRepository.salvar(inativo)

        veiculos = VeiculoRepository.listar_ativos()

        placas = {veiculo.placa for veiculo in veiculos}

        assert "CCC3C33" in placas
        assert "DDD4D44" not in placas


def test_listar_veiculos_por_cliente(app):
    with app.app_context():
        primeiro_cliente = criar_cliente(
            nome_razao_social="Primeiro Cliente"
        )
        segundo_cliente = criar_cliente(
            nome_razao_social="Segundo Cliente"
        )

        marca = criar_marca()
        modelo = criar_modelo(marca)
        porte = criar_porte()

        primeiro_veiculo = criar_veiculo(
            cliente=primeiro_cliente,
            modelo=modelo,
            porte=porte,
            placa="EEE5E55",
        )

        segundo_veiculo = criar_veiculo(
            cliente=segundo_cliente,
            modelo=modelo,
            porte=porte,
            placa="FFF6F66",
        )

        VeiculoRepository.salvar(primeiro_veiculo)
        VeiculoRepository.salvar(segundo_veiculo)

        veiculos = VeiculoRepository.listar_por_cliente(
            primeiro_cliente.id
        )

        assert len(veiculos) == 1
        assert veiculos[0].id == primeiro_veiculo.id
        assert veiculos[0].placa == "EEE5E55"


def test_excluir_veiculo(app):
    with app.app_context():
        cliente, _, modelo, porte = preparar_dependencias()

        veiculo = criar_veiculo(
            cliente=cliente,
            modelo=modelo,
            porte=porte,
            placa="GGG7G77",
        )

        VeiculoRepository.salvar(veiculo)

        veiculo_id = veiculo.id

        VeiculoRepository.excluir(veiculo)

        encontrado = VeiculoRepository.buscar_por_id(
            veiculo_id
        )

        assert encontrado is None