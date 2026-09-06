from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)

from ..extensions import db
from ..models.cliente import Cliente
from ..models.modelo import Modelo
from ..models.porte_veiculo import PorteVeiculo
from ..services.veiculo_service import VeiculoService


veiculo_web_bp = Blueprint(
    "veiculo_web",
    __name__,
)


@veiculo_web_bp.get("/veiculos")
def gestao_veiculos():
    veiculos = VeiculoService.listar_todos()

    clientes = (
        db.session.query(Cliente)
        .order_by(Cliente.nome_razao_social)
        .all()
    )

    modelos = (
        db.session.query(Modelo)
        .order_by(Modelo.nome)
        .all()
    )

    portes = (
        db.session.query(PorteVeiculo)
        .order_by(PorteVeiculo.nome)
        .all()
    )

    return render_template(
        "veiculos.html",
        veiculos=veiculos,
        clientes=clientes,
        modelos=modelos,
        portes=portes,
    )


@veiculo_web_bp.post("/veiculos")
def criar_veiculo():
    dados = {
        "cliente_id": int(request.form["cliente_id"]),
        "modelo_id": int(request.form["modelo_id"]),
        "porte_id": int(request.form["porte_id"]),
        "placa": request.form.get(
            "placa",
            "",
        ).strip().upper(),
        "cor": request.form.get(
            "cor",
            "",
        ).strip(),
        "ano_fabricacao": request.form.get(
            "ano_fabricacao",
            "",
        ).strip()
        or None,
        "ano_modelo": request.form.get(
            "ano_modelo",
            "",
        ).strip()
        or None,
        "renavam": request.form.get(
            "renavam",
            "",
        ).strip()
        or None,
        "chassi": request.form.get(
            "chassi",
            "",
        ).strip()
        or None,
        "observacoes": request.form.get(
            "observacoes",
            "",
        ).strip()
        or None,
    }

    campos_obrigatorios = (
        "cliente_id",
        "modelo_id",
        "porte_id",
        "placa",
        "cor",
    )

    if any(
        not dados[campo]
        for campo in campos_obrigatorios
    ):
        return _renderizar_com_erro(
            "Preencha todos os campos obrigatórios.",
            400,
        )

    try:
        VeiculoService.criar(dados)
        db.session.commit()

    except Exception:
        db.session.rollback()

        return _renderizar_com_erro(
            "Não foi possível cadastrar o veículo. "
            "Verifique os dados informados.",
            400,
        )

    return redirect(
        url_for("veiculo_web.gestao_veiculos")
    )


def _renderizar_com_erro(
    mensagem: str,
    status_code: int,
):
    return (
        render_template(
            "veiculos.html",
            veiculos=VeiculoService.listar_todos(),
            clientes=(
                db.session.query(Cliente)
                .order_by(Cliente.nome_razao_social)
                .all()
            ),
            modelos=(
                db.session.query(Modelo)
                .order_by(Modelo.nome)
                .all()
            ),
            portes=(
                db.session.query(PorteVeiculo)
                .order_by(PorteVeiculo.nome)
                .all()
            ),
            erro=mensagem,
        ),
        status_code,
    )