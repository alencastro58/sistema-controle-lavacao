from flask import Blueprint, render_template


ordem_servico_web_bp = Blueprint(
    "ordem_servico_web",
    __name__,
)


@ordem_servico_web_bp.get("/ordens-servico/gestao")
def gestao_ordens_servico():
    return render_template("ordens_servico.html")
