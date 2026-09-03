from flask import Blueprint, jsonify, request

from ..extensions import db
from ..services.ordem_servico_service import OrdemServicoService


ordem_servico_bp = Blueprint(
    "ordem_servico",
    __name__,
)


def _ordem_servico_para_json(ordem_servico) -> dict:
    return {
        "id": ordem_servico.id,
        "numero": ordem_servico.numero,
        "cliente_id": ordem_servico.cliente_id,
        "veiculo_id": ordem_servico.veiculo_id,
        "data_agendamento": (
            ordem_servico.data_agendamento.isoformat()
            if ordem_servico.data_agendamento
            else None
        ),
        "valor_total": (
            float(ordem_servico.valor_total)
            if ordem_servico.valor_total is not None
            else 0
        ),
        "desconto": (
            float(ordem_servico.desconto)
            if ordem_servico.desconto is not None
            else 0
        ),
        "status": ordem_servico.status,
        "observacoes": ordem_servico.observacoes,
        "criado_em": ordem_servico.criado_em.isoformat(),
        "atualizado_em": ordem_servico.atualizado_em.isoformat(),
    }


@ordem_servico_bp.get("/ordens-servico")
def listar_ordens_servico():
    ordens_servico = OrdemServicoService.listar_todas()

    return jsonify(
        [
            _ordem_servico_para_json(ordem_servico)
            for ordem_servico in ordens_servico
        ]
    ), 200


@ordem_servico_bp.post("/ordens-servico")
def criar_ordem_servico():
    dados = request.get_json(silent=True) or {}

    campos_obrigatorios = [
        "numero",
        "cliente_id",
        "veiculo_id",
    ]

    for campo in campos_obrigatorios:
        if dados.get(campo) is None:
            return jsonify(
                {
                    "erro": f"{campo} é obrigatório.",
                }
            ), 400

    ordem_servico = OrdemServicoService.criar(dados)

    db.session.commit()

    return jsonify(
        _ordem_servico_para_json(ordem_servico)
    ), 201


@ordem_servico_bp.get("/ordens-servico/<int:ordem_servico_id>")
def buscar_ordem_servico(ordem_servico_id: int):
    ordem_servico = OrdemServicoService.buscar_por_id(
        ordem_servico_id
    )

    if ordem_servico is None:
        return jsonify(
            {
                "erro": "Ordem de Serviço não encontrada.",
            }
        ), 404

    return jsonify(
        _ordem_servico_para_json(ordem_servico)
    ), 200


@ordem_servico_bp.delete("/ordens-servico/<int:ordem_servico_id>")
def excluir_ordem_servico(ordem_servico_id: int):
    ordem_servico = OrdemServicoService.buscar_por_id(
        ordem_servico_id
    )

    if ordem_servico is None:
        return jsonify(
            {
                "erro": "Ordem de Serviço não encontrada.",
            }
        ), 404

    OrdemServicoService.excluir(ordem_servico)

    db.session.commit()

    return "", 204
