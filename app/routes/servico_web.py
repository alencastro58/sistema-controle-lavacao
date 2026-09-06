from decimal import Decimal, InvalidOperation

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)

from ..extensions import db
from ..models.porte_veiculo import PorteVeiculo
from ..models.servico import Servico
from ..services.preco_servico_service import PrecoServicoService


servico_web_bp = Blueprint(
    "servico_web",
    __name__,
)


@servico_web_bp.get("/servicos")
def gestao_servicos():
    servicos = (
        db.session.query(Servico)
        .order_by(Servico.nome)
        .all()
    )

    portes = (
        db.session.query(PorteVeiculo)
        .filter(PorteVeiculo.ativo.is_(True))
        .order_by(PorteVeiculo.ordem, PorteVeiculo.nome)
        .all()
    )

    precos = PrecoServicoService.listar_todos()

    return render_template(
        "servicos.html",
        servicos=servicos,
        portes=portes,
        precos=precos,
    )


@servico_web_bp.post("/servicos/precos")
def criar_preco():
    servico_id = request.form.get("servico_id", "").strip()
    porte_id = request.form.get("porte_id", "").strip()
    valor = request.form.get("valor", "").strip().replace(",", ".")

    if not servico_id or not porte_id or not valor:
        return _renderizar_com_erro(
            "Preencha serviço, porte e valor.",
            400,
        )

    try:
        valor_decimal = Decimal(valor)

        if valor_decimal < 0:
            raise InvalidOperation

        dados = {
            "servico_id": int(servico_id),
            "porte_id": int(porte_id),
            "valor": valor_decimal,
            "ativo": True,
        }

        PrecoServicoService.criar(dados)
        db.session.commit()

    except (ValueError, InvalidOperation):
        db.session.rollback()

        return _renderizar_com_erro(
            "Informe um valor válido e não negativo.",
            400,
        )

    except Exception:
        db.session.rollback()

        return _renderizar_com_erro(
            "Não foi possível cadastrar o preço. "
            "Verifique se já existe preço para esse serviço e porte.",
            400,
        )

    return redirect(url_for("servico_web.gestao_servicos"))


@servico_web_bp.post("/servicos/precos/<int:preco_servico_id>/excluir")
def excluir_preco(preco_servico_id: int):
    try:
        PrecoServicoService.excluir(preco_servico_id)
        db.session.commit()

    except Exception:
        db.session.rollback()

        return _renderizar_com_erro(
            "Não foi possível excluir o preço informado.",
            400,
        )

    return redirect(url_for("servico_web.gestao_servicos"))


def _renderizar_com_erro(
    mensagem: str,
    status_code: int,
):
    servicos = (
        db.session.query(Servico)
        .order_by(Servico.nome)
        .all()
    )

    portes = (
        db.session.query(PorteVeiculo)
        .filter(PorteVeiculo.ativo.is_(True))
        .order_by(PorteVeiculo.ordem, PorteVeiculo.nome)
        .all()
    )

    precos = PrecoServicoService.listar_todos()

    return (
        render_template(
            "servicos.html",
            servicos=servicos,
            portes=portes,
            precos=precos,
            erro=mensagem,
        ),
        status_code,
    )
