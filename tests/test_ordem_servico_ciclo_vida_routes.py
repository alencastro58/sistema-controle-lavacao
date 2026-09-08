import uuid
from datetime import datetime
from decimal import Decimal

import pytest

from app.extensions import db
from app.models import (
    Cliente,
    Marca,
    Modelo,
    MovimentacaoFidelidade,
    OrdemServico,
    PorteVeiculo,
    ProgramaFidelidade,
    SaldoFidelidade,
    Veiculo,
)


@pytest.fixture
def ordem_servico_ciclo_dados(app_context):
    identificador = uuid.uuid4().hex[:8]

    cliente = Cliente(
        tipo_pessoa="PF",
        nome_razao_social=f"Cliente Ciclo {identificador}",
        email=f"ciclo.{identificador}@exemplo.com",
        telefone="48980000007",
    )

    marca = Marca(
        nome=f"Marca Ciclo {identificador}",
    )

    porte = PorteVeiculo(
        nome=f"Porte Ciclo {identificador}",
        ordem=93,
    )

    programa = ProgramaFidelidade(
        habilitado=True,
        pontos_por_real=Decimal("1.00"),
        valor_por_ponto=Decimal("1.00"),
        desconto_maximo_percentual=Decimal("50.00"),
    )

    db.session.add_all(
        [
            cliente,
            marca,
            porte,
            programa,
        ]
    )

    db.session.flush()

    modelo = Modelo(
        marca_id=marca.id,
        nome=f"Modelo Ciclo {identificador}",
    )

    db.session.add(modelo)
    db.session.flush()

    veiculo = Veiculo(
        cliente_id=cliente.id,
        modelo_id=modelo.id,
        porte_id=porte.id,
        placa=f"C{identificador[:6]}",
        cor="Preto",
    )

    db.session.add(veiculo)
    db.session.flush()

    ordem_servico = OrdemServico(
        numero=f"OS-CICLO-{identificador}",
        cliente_id=cliente.id,
        veiculo_id=veiculo.id,
        valor_total=Decimal("150.00"),
        desconto=Decimal("0.00"),
        status="ABERTA",
        criado_em=datetime.now(),
        atualizado_em=datetime.now(),
    )

    db.session.add(ordem_servico)
    db.session.commit()

    dados = {
        "cliente_id": cliente.id,
        "marca_id": marca.id,
        "modelo_id": modelo.id,
        "porte_id": porte.id,
        "veiculo_id": veiculo.id,
        "ordem_servico_id": ordem_servico.id,
        "programa_id": programa.id,
    }

    yield dados

    db.session.rollback()

    movimentacoes = db.session.query(
        MovimentacaoFidelidade
    ).filter_by(
        programa_id=dados["programa_id"],
    ).all()

    for movimentacao in movimentacoes:
        db.session.delete(movimentacao)

    db.session.flush()

    saldo = db.session.query(
        SaldoFidelidade
    ).filter_by(
        programa_id=dados["programa_id"],
    ).first()

    if saldo is not None:
        db.session.delete(saldo)

    db.session.flush()

    ordem = db.session.get(
        OrdemServico,
        dados["ordem_servico_id"],
    )

    if ordem is not None:
        db.session.delete(ordem)

    db.session.flush()

    programa = db.session.get(
        ProgramaFidelidade,
        dados["programa_id"],
    )

    if programa is not None:
        db.session.delete(programa)

    db.session.flush()

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


def test_alterar_status_para_em_andamento(
    client,
    ordem_servico_ciclo_dados,
):
    ordem_id = ordem_servico_ciclo_dados["ordem_servico_id"]

    response = client.patch(
        f"/ordens-servico/{ordem_id}/status",
        json={"status": "EM_ANDAMENTO"},
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "EM_ANDAMENTO"


def test_confirmar_pagamento_registra_pagamento_e_entrega(
    client,
    ordem_servico_ciclo_dados,
):
    ordem_id = ordem_servico_ciclo_dados["ordem_servico_id"]

    response = client.post(
        f"/ordens-servico/{ordem_id}/confirmar-pagamento",
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["pagamento_confirmado"] is True
    assert data["pagamento_confirmado_em"] is not None
    assert data["veiculo_entregue"] is True
    assert data["veiculo_entregue_em"] is not None


def test_confirmar_pagamento_credita_fidelidade(
    client,
    app_context,
    ordem_servico_ciclo_dados,
):
    ordem_id = ordem_servico_ciclo_dados["ordem_servico_id"]
    programa_id = ordem_servico_ciclo_dados["programa_id"]
    cliente_id = ordem_servico_ciclo_dados["cliente_id"]

    response = client.post(
        f"/ordens-servico/{ordem_id}/confirmar-pagamento",
    )

    assert response.status_code == 200

    saldo = db.session.query(
        SaldoFidelidade
    ).filter_by(
        programa_id=programa_id,
        cliente_id=cliente_id,
    ).first()

    assert saldo is not None
    assert saldo.saldo_pontos == Decimal("150.00")
    assert saldo.total_acumulado == Decimal("150.00")
    assert saldo.total_utilizado == Decimal("0.00")

    movimentacao = db.session.query(
        MovimentacaoFidelidade
    ).filter_by(
        programa_id=programa_id,
        cliente_id=cliente_id,
        ordem_servico_id=ordem_id,
        tipo="CREDITO",
    ).first()

    assert movimentacao is not None
    assert movimentacao.pontos == Decimal("150.00")
    assert movimentacao.valor_base == Decimal("150.00")


def test_confirmar_pagamento_nao_credita_fidelidade_duas_vezes(
    client,
    app_context,
    ordem_servico_ciclo_dados,
):
    ordem_id = ordem_servico_ciclo_dados["ordem_servico_id"]
    programa_id = ordem_servico_ciclo_dados["programa_id"]
    cliente_id = ordem_servico_ciclo_dados["cliente_id"]

    primeira_resposta = client.post(
        f"/ordens-servico/{ordem_id}/confirmar-pagamento",
    )

    assert primeira_resposta.status_code == 200

    segunda_resposta = client.post(
        f"/ordens-servico/{ordem_id}/confirmar-pagamento",
    )

    assert segunda_resposta.status_code == 400

    saldo = db.session.query(
        SaldoFidelidade
    ).filter_by(
        programa_id=programa_id,
        cliente_id=cliente_id,
    ).first()

    assert saldo is not None
    assert saldo.saldo_pontos == Decimal("150.00")
    assert saldo.total_acumulado == Decimal("150.00")

    movimentacoes = db.session.query(
        MovimentacaoFidelidade
    ).filter_by(
        programa_id=programa_id,
        cliente_id=cliente_id,
        ordem_servico_id=ordem_id,
        tipo="CREDITO",
    ).all()

    assert len(movimentacoes) == 1


def test_confirmar_pagamento_nao_credita_ordem_cancelada(
    client,
    app_context,
    ordem_servico_ciclo_dados,
):
    ordem_id = ordem_servico_ciclo_dados["ordem_servico_id"]
    programa_id = ordem_servico_ciclo_dados["programa_id"]
    cliente_id = ordem_servico_ciclo_dados["cliente_id"]

    cancelar_response = client.patch(
        f"/ordens-servico/{ordem_id}/status",
        json={"status": "CANCELADA"},
    )

    assert cancelar_response.status_code == 200

    pagamento_response = client.post(
        f"/ordens-servico/{ordem_id}/confirmar-pagamento",
    )

    assert pagamento_response.status_code == 400

    saldo = db.session.query(
        SaldoFidelidade
    ).filter_by(
        programa_id=programa_id,
        cliente_id=cliente_id,
    ).first()

    assert saldo is None

    movimentacoes = db.session.query(
        MovimentacaoFidelidade
    ).filter_by(
        programa_id=programa_id,
        cliente_id=cliente_id,
        ordem_servico_id=ordem_id,
    ).all()

    assert movimentacoes == []


def test_concluir_exige_pagamento_confirmado(
    client,
    ordem_servico_ciclo_dados,
):
    ordem_id = ordem_servico_ciclo_dados["ordem_servico_id"]

    response = client.patch(
        f"/ordens-servico/{ordem_id}/status",
        json={"status": "CONCLUIDA"},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "transição de status não permitida" in data["erro"].lower()


def test_cancelar_ordem_aberta(
    client,
    ordem_servico_ciclo_dados,
):
    ordem_id = ordem_servico_ciclo_dados["ordem_servico_id"]

    response = client.patch(
        f"/ordens-servico/{ordem_id}/status",
        json={"status": "CANCELADA"},
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "CANCELADA"


def test_confirmar_pagamento_ordem_inexistente(
    client,
):
    response = client.post(
        "/ordens-servico/999999/confirmar-pagamento",
    )

    assert response.status_code == 404


def test_alterar_status_ordem_inexistente(
    client,
):
    response = client.patch(
        "/ordens-servico/999999/status",
        json={"status": "EM_ANDAMENTO"},
    )

    assert response.status_code == 404


def test_status_obrigatorio(
    client,
    ordem_servico_ciclo_dados,
):
    ordem_id = ordem_servico_ciclo_dados["ordem_servico_id"]

    response = client.patch(
        f"/ordens-servico/{ordem_id}/status",
        json={},
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["erro"] == "status é obrigatório."