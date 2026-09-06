from datetime import date

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)

from ..extensions import db
from ..services.cliente_service import ClienteService


cliente_web_bp = Blueprint(
    "cliente_web",
    __name__,
)


@cliente_web_bp.get("/clientes")
def gestao_clientes():
    clientes = ClienteService.listar_todos()

    return render_template(
        "clientes.html",
        clientes=clientes,
    )


@cliente_web_bp.post("/clientes")
def criar_cliente():
    dados = {
        "tipo_pessoa": request.form.get(
            "tipo_pessoa",
            "",
        ).strip(),
        "nome_razao_social": request.form.get(
            "nome_razao_social",
            "",
        ).strip(),
        "nome_fantasia": request.form.get(
            "nome_fantasia",
            "",
        ).strip()
        or None,
        "cpf_cnpj": request.form.get(
            "cpf_cnpj",
            "",
        ).strip()
        or None,
        "email": request.form.get(
            "email",
            "",
        ).strip(),
        "telefone": request.form.get(
            "telefone",
            "",
        ).strip(),
        "inscricao_estadual": request.form.get(
            "inscricao_estadual",
            "",
        ).strip()
        or None,
        "data_nascimento": None,
        "cep": request.form.get(
            "cep",
            "",
        ).strip()
        or None,
        "logradouro": request.form.get(
            "logradouro",
            "",
        ).strip()
        or None,
        "numero": request.form.get(
            "numero",
            "",
        ).strip()
        or None,
        "complemento": request.form.get(
            "complemento",
            "",
        ).strip()
        or None,
        "bairro": request.form.get(
            "bairro",
            "",
        ).strip()
        or None,
        "cidade": request.form.get(
            "cidade",
            "",
        ).strip()
        or None,
        "uf": request.form.get(
            "uf",
            "",
        ).strip()
        or None,
    }

    data_nascimento = request.form.get(
        "data_nascimento",
        "",
    ).strip()

    if data_nascimento:
        dados["data_nascimento"] = date.fromisoformat(
            data_nascimento
        )

    campos_obrigatorios = (
        "tipo_pessoa",
        "nome_razao_social",
        "email",
        "telefone",
    )

    if any(
        not dados[campo]
        for campo in campos_obrigatorios
    ):
        clientes = ClienteService.listar_todos()

        return render_template(
            "clientes.html",
            clientes=clientes,
            erro=(
                "Preencha os campos obrigatórios: "
                "tipo de pessoa, nome/razão social, "
                "e-mail e telefone."
            ),
        ), 400

    try:
        ClienteService.criar(dados)
        db.session.commit()

    except Exception:
        db.session.rollback()

        clientes = ClienteService.listar_todos()

        return render_template(
            "clientes.html",
            clientes=clientes,
            erro=(
                "Não foi possível cadastrar o cliente. "
                "Verifique os dados informados."
            ),
        ), 400

    return redirect(
        url_for("cliente_web.gestao_clientes")
    )