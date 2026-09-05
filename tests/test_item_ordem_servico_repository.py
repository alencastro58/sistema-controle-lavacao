import uuid

import pytest

from app.extensions import db
from app.models import (
    Cliente,
    Marca,
    Modelo,
    OrdemServico,
    PorteVeiculo,
    Servico,
    Veiculo,
    ItemOrdemServico,
)
from app.repositories.item_ordem_servico_repository import (
    ItemOrdemServicoRepository,
)


@pytest.fixture
def item_ordem_servico_dados(app_context):
    sufixo = uuid.uuid4().hex[:8]

    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=f"Cliente Item OS {sufixo}",
        email=f"cliente.item.os.{sufixo}@exemplo.com",
        telefone="48984444444",
    )

    marca = Marca(
        nome=f"Marca Item OS {sufixo}",
    )

    porte = PorteVeiculo(
        nome=f"Porte Item OS {sufixo}",
        ordem=98,
    )

    servico = Servico(
        nome=f"Servico Item OS {sufixo}",
        descricao="Servico para teste de itens da OS",
        valor=0,
        ativo=True,
    )

    db.session.add_all(
        [
            cliente,
            marca,
            porte,
            servico,
        ]
    )
    db.session.flush()

    modelo = Modelo(
        marca_id=marca.id,
        nome=f"Modelo Item OS {sufixo}",
    )

    db.session.add(modelo)
    db.session.flush()

    veiculo = Veiculo(
        cliente_id=cliente.id,
        modelo_id=modelo.id,
        porte_id=porte.id,
        placa=f"ITO{str(uuid.uuid4().int)[-4:]}",
        cor="Branco",
    )

    db.session.add(veiculo)
    db.session.flush()

    ordem = OrdemServico(
        numero=f"OS-ITEM-{sufixo}",
        cliente_id=cliente.id,
        veiculo_id=veiculo.id,
        valor_total=0,
        desconto=0,
        status="ABERTA",
    )

    db.session.add(ordem)
    db.session.flush()

    item_1 = ItemOrdemServico(
        ordem_servico_id=ordem.id,
        servico_id=servico.id,
        quantidade=1,
        valor_unitario=50.00,
        desconto=0,
    )

    item_2 = ItemOrdemServico(
        ordem_servico_id=ordem.id,
        servico_id=servico.id,
        quantidade=2,
        valor_unitario=40.00,
        desconto=5.00,
    )

    db.session.add_all(
        [
            item_1,
            item_2,
        ]
    )
    db.session.flush()

    dados = {
        "cliente_id": cliente.id,
        "marca_id": marca.id,
        "modelo_id": modelo.id,
        "porte_id": porte.id,
        "veiculo_id": veiculo.id,
        "servico_id": servico.id,
        "ordem_servico_id": ordem.id,
        "item_1_id": item_1.id,
        "item_2_id": item_2.id,
    }

    db.session.commit()

    yield dados

    db.session.rollback()

    for item_id in [
        dados["item_1_id"],
        dados["item_2_id"],
    ]:
        item = db.session.get(
            ItemOrdemServico,
            item_id,
        )

        if item is not None:
            db.session.delete(item)

    ordem = db.session.get(
        OrdemServico,
        dados["ordem_servico_id"],
    )

    if ordem is not None:
        db.session.delete(ordem)

    veiculo = db.session.get(
        Veiculo,
        dados["veiculo_id"],
    )

    if veiculo is not None:
        db.session.delete(veiculo)

    modelo = db.session.get(
        Modelo,
        dados["modelo_id"],
    )

    if modelo is not None:
        db.session.delete(modelo)

    servico = db.session.get(
        Servico,
        dados["servico_id"],
    )

    if servico is not None:
        db.session.delete(servico)

    porte = db.session.get(
        PorteVeiculo,
        dados["porte_id"],
    )

    if porte is not None:
        db.session.delete(porte)

    marca = db.session.get(
        Marca,
        dados["marca_id"],
    )

    if marca is not None:
        db.session.delete(marca)

    cliente = db.session.get(
        Cliente,
        dados["cliente_id"],
    )

    if cliente is not None:
        db.session.delete(cliente)

    db.session.commit()


@pytest.mark.usefixtures("app_context")
def test_salvar_item_ordem_servico(item_ordem_servico_dados):
    item = ItemOrdemServico(
        ordem_servico_id=item_ordem_servico_dados["ordem_servico_id"],
        servico_id=item_ordem_servico_dados["servico_id"],
        quantidade=1,
        valor_unitario=60.00,
        desconto=0,
    )

    resultado = ItemOrdemServicoRepository.salvar(item)

    assert resultado is item
    assert item.id is not None

    db.session.rollback()


@pytest.mark.usefixtures("app_context")
def test_buscar_item_ordem_servico_por_id(item_ordem_servico_dados):
    resultado = ItemOrdemServicoRepository.buscar_por_id(
        item_ordem_servico_dados["item_1_id"]
    )

    assert resultado is not None
    assert resultado.id == item_ordem_servico_dados["item_1_id"]


@pytest.mark.usefixtures("app_context")
def test_buscar_item_ordem_servico_por_id_retorna_none_quando_nao_encontrado():
    resultado = ItemOrdemServicoRepository.buscar_por_id(999999)

    assert resultado is None


@pytest.mark.usefixtures("app_context")
def test_listar_itens_por_ordem_servico(item_ordem_servico_dados):
    lista = ItemOrdemServicoRepository.listar_por_ordem_servico(
        item_ordem_servico_dados["ordem_servico_id"]
    )

    assert len(lista) == 2

    assert {item.id for item in lista} == {
        item_ordem_servico_dados["item_1_id"],
        item_ordem_servico_dados["item_2_id"],
    }


@pytest.mark.usefixtures("app_context")
def test_excluir_item_ordem_servico(item_ordem_servico_dados):
    item = ItemOrdemServicoRepository.buscar_por_id(
        item_ordem_servico_dados["item_1_id"]
    )

    assert item is not None

    ItemOrdemServicoRepository.excluir(item)
    db.session.commit()

    resultado = ItemOrdemServicoRepository.buscar_por_id(
        item_ordem_servico_dados["item_1_id"]
    )

    assert resultado is None
