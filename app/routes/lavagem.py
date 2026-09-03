from flask import Blueprint, jsonify, request

from ..extensions import db
from ..models.ordem_servico import OrdemServico
from ..models.lavagem import Lavagem
from ..repositories.lavagem_repository import LavagemRepository
from ..services.lavagem_service import LavagemService


lavagem_bp = Blueprint("lavagem", __name__)


def _lavagem_para_json(lavagem) -> dict:
    return {
        "id": lavagem.id,
        "ordem_servico_id": lavagem.ordem_servico_id,
        "inicio": lavagem.inicio.isoformat() if lavagem.inicio else None,
        "fim": lavagem.fim.isoformat() if lavagem.fim else None,
        "status": lavagem.status,
        "observacoes": lavagem.observacoes,
        "criado_em": lavagem.criado_em.isoformat(),
        "atualizado_em": lavagem.atualizado_em.isoformat(),
    }


@lavagem_bp.get("/lavagens")
def listar_lavagens():
    lavagens = LavagemRepository.listar_todas()

    return jsonify(
        [
            _lavagem_para_json(lavagem)
            for lavagem in lavagens
        ]
    ), 200


@lavagem_bp.post("/lavagens")
def criar_lavagem():
    dados = request.get_json(silent=True) or {}

    ordem_servico_id = dados.get("ordem_servico_id")

    if ordem_servico_id is None:
        return jsonify(
            {
                "erro": "ordem_servico_id é obrigatório.",
            }
        ), 400

    ordem_servico = db.session.get(
        OrdemServico,
        ordem_servico_id,
    )

    if ordem_servico is None:
        return jsonify(
            {
                "erro": "Ordem de Serviço não encontrada.",
            }
        ), 404

    lavagem = Lavagem(
        ordem_servico_id=ordem_servico.id,
        status=LavagemService.STATUS_AGUARDANDO,
        observacoes=dados.get("observacoes"),
    )

    LavagemRepository.salvar(lavagem)
    db.session.commit()

    return jsonify(_lavagem_para_json(lavagem)), 201


@lavagem_bp.get("/lavagens/<int:lavagem_id>")
def buscar_lavagem(lavagem_id: int):
    lavagem = LavagemRepository.buscar_por_id(lavagem_id)

    if lavagem is None:
        return jsonify(
            {
                "erro": "Lavagem não encontrada.",
            }
        ), 404

    return jsonify(_lavagem_para_json(lavagem))


@lavagem_bp.get("/ordens-servico/<int:ordem_servico_id>/lavagens")
def listar_lavagens_por_ordem_servico(
    ordem_servico_id: int,
):
    lavagens = LavagemRepository.listar_por_ordem_servico(
        ordem_servico_id
    )

    return jsonify(
        [
            _lavagem_para_json(lavagem)
            for lavagem in lavagens
        ]
    ), 200


@lavagem_bp.post("/lavagens/<int:lavagem_id>/iniciar")
def iniciar_lavagem(lavagem_id: int):
    lavagem = LavagemRepository.buscar_por_id(lavagem_id)

    if lavagem is None:
        return jsonify(
            {
                "erro": "Lavagem não encontrada.",
            }
        ), 404

    try:
        LavagemService.iniciar(lavagem)
        db.session.commit()
    except ValueError as exc:
        db.session.rollback()

        return jsonify(
            {
                "erro": str(exc),
            }
        ), 400

    return jsonify(_lavagem_para_json(lavagem)), 200


@lavagem_bp.post("/lavagens/<int:lavagem_id>/concluir")
def concluir_lavagem(lavagem_id: int):
    lavagem = LavagemRepository.buscar_por_id(lavagem_id)

    if lavagem is None:
        return jsonify(
            {
                "erro": "Lavagem não encontrada.",
            }
        ), 404

    try:
        LavagemService.concluir(lavagem)
        db.session.commit()
    except ValueError as exc:
        db.session.rollback()

        return jsonify(
            {
                "erro": str(exc),
            }
        ), 400

    return jsonify(_lavagem_para_json(lavagem)), 200


@lavagem_bp.post("/lavagens/<int:lavagem_id>/cancelar")
def cancelar_lavagem(lavagem_id: int):
    lavagem = LavagemRepository.buscar_por_id(lavagem_id)

    if lavagem is None:
        return jsonify(
            {
                "erro": "Lavagem não encontrada.",
            }
        ), 404

    try:
        LavagemService.cancelar(lavagem)
        db.session.commit()
    except ValueError as exc:
        db.session.rollback()

        return jsonify(
            {
                "erro": str(exc),
            }
        ), 400

    return jsonify(_lavagem_para_json(lavagem)), 200