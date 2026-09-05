from flask import Blueprint, jsonify, request

from ..extensions import db
from ..services.preco_servico_service import PrecoServicoService


preco_servico_bp = Blueprint(
    "preco_servico",
    __name__,
)


def _preco_servico_para_json(preco_servico) -> dict:
    return {
        "id": preco_servico.id,
        "servico_id": preco_servico.servico_id,
        "porte_id": preco_servico.porte_id,
        "valor": (
            float(preco_servico.valor)
            if preco_servico.valor is not None
            else 0
        ),
        "ativo": preco_servico.ativo,
        "criado_em": preco_servico.criado_em.isoformat(),
        "atualizado_em": preco_servico.atualizado_em.isoformat(),
    }


@preco_servico_bp.get("/precos-servicos")
def listar_precos_servicos():
    precos_servicos = PrecoServicoService.listar_todos()

    return jsonify(
        [
            _preco_servico_para_json(preco_servico)
            for preco_servico in precos_servicos
        ]
    ), 200


@preco_servico_bp.post("/precos-servicos")
def criar_preco_servico():
    dados = request.get_json(silent=True) or {}

    campos_obrigatorios = [
        "servico_id",
        "porte_id",
        "valor",
    ]

    for campo in campos_obrigatorios:
        if dados.get(campo) is None:
            return jsonify(
                {
                    "erro": f"{campo} é obrigatório.",
                }
            ), 400

    preco_servico = PrecoServicoService.criar(dados)

    db.session.commit()

    return jsonify(
        _preco_servico_para_json(preco_servico)
    ), 201


@preco_servico_bp.get("/precos-servicos/<int:preco_servico_id>")
def buscar_preco_servico(preco_servico_id: int):
    preco_servico = PrecoServicoService.buscar_por_id(
        preco_servico_id
    )

    if preco_servico is None:
        return jsonify(
            {
                "erro": "Preço de Serviço não encontrado.",
            }
        ), 404

    return jsonify(
        _preco_servico_para_json(preco_servico)
    ), 200


@preco_servico_bp.delete("/precos-servicos/<int:preco_servico_id>")
def excluir_preco_servico(preco_servico_id: int):
    preco_servico = PrecoServicoService.buscar_por_id(
        preco_servico_id
    )

    if preco_servico is None:
        return jsonify(
            {
                "erro": "Preço de Serviço não encontrado.",
            }
        ), 404

    PrecoServicoService.excluir(preco_servico)

    db.session.commit()

    return "", 204
