from datetime import datetime, timezone

from ..extensions import db
from ..models.lavagem import Lavagem


class LavagemService:
    STATUS_AGUARDANDO = "AGUARDANDO"
    STATUS_EM_ANDAMENTO = "EM_ANDAMENTO"
    STATUS_CONCLUIDA = "CONCLUIDA"
    STATUS_CANCELADA = "CANCELADA"

    STATUS_VALIDOS = {
        STATUS_AGUARDANDO,
        STATUS_EM_ANDAMENTO,
        STATUS_CONCLUIDA,
        STATUS_CANCELADA,
    }

    TRANSICOES_PERMITIDAS = {
        STATUS_AGUARDANDO: {
            STATUS_EM_ANDAMENTO,
            STATUS_CANCELADA,
        },
        STATUS_EM_ANDAMENTO: {
            STATUS_CONCLUIDA,
            STATUS_CANCELADA,
        },
        STATUS_CONCLUIDA: set(),
        STATUS_CANCELADA: set(),
    }

    @classmethod
    def iniciar(cls, lavagem: Lavagem) -> Lavagem:
        cls._alterar_status(
            lavagem,
            cls.STATUS_EM_ANDAMENTO,
        )

        lavagem.inicio = datetime.now(timezone.utc)

        db.session.flush()

        return lavagem

    @classmethod
    def concluir(cls, lavagem: Lavagem) -> Lavagem:
        cls._alterar_status(
            lavagem,
            cls.STATUS_CONCLUIDA,
        )

        lavagem.fim = datetime.now(timezone.utc)

        db.session.flush()

        return lavagem

    @classmethod
    def cancelar(cls, lavagem: Lavagem) -> Lavagem:
        cls._alterar_status(
            lavagem,
            cls.STATUS_CANCELADA,
        )

        db.session.flush()

        return lavagem

    @classmethod
    def _alterar_status(
        cls,
        lavagem: Lavagem,
        novo_status: str,
    ) -> None:
        if novo_status not in cls.STATUS_VALIDOS:
            raise ValueError(
                f"Status de lavagem inválido: {novo_status}"
            )

        status_atual = lavagem.status

        if novo_status == status_atual:
            raise ValueError(
                f"A lavagem já está com o status {status_atual}."
            )

        transicoes = cls.TRANSICOES_PERMITIDAS.get(
            status_atual,
            set(),
        )

        if novo_status not in transicoes:
            raise ValueError(
                f"Transição de status não permitida: "
                f"{status_atual} -> {novo_status}."
            )

        lavagem.status = novo_status