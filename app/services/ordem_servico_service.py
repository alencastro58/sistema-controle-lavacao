from datetime import datetime, timezone

from ..models.ordem_servico import OrdemServico
from ..repositories.ordem_servico_repository import OrdemServicoRepository


class OrdemServicoService:
    STATUS_ABERTA = "ABERTA"
    STATUS_EM_ANDAMENTO = "EM_ANDAMENTO"
    STATUS_CONCLUIDA = "CONCLUIDA"
    STATUS_CANCELADA = "CANCELADA"

    TRANSICOES_PERMITIDAS = {
        STATUS_ABERTA: {
            STATUS_EM_ANDAMENTO,
            STATUS_CANCELADA,
        },
        STATUS_EM_ANDAMENTO: {
            STATUS_CONCLUIDA,
        },
        STATUS_CONCLUIDA: set(),
        STATUS_CANCELADA: set(),
    }

    @staticmethod
    def criar(dados: dict) -> OrdemServico:
        ordem_servico = OrdemServico(
            numero=dados["numero"],
            cliente_id=dados["cliente_id"],
            veiculo_id=dados["veiculo_id"],
            data_agendamento=dados.get("data_agendamento"),
            valor_total=dados.get("valor_total", 0),
            desconto=dados.get("desconto", 0),
            status=OrdemServicoService.STATUS_ABERTA,
            observacoes=dados.get("observacoes"),
        )

        return OrdemServicoRepository.salvar(
            ordem_servico
        )

    @staticmethod
    def buscar_por_id(
        ordem_servico_id: int,
    ):
        return OrdemServicoRepository.buscar_por_id(
            ordem_servico_id
        )

    @staticmethod
    def listar_todas():
        return OrdemServicoRepository.listar_todas()

    @staticmethod
    def listar_por_cliente(
        cliente_id: int,
    ):
        return OrdemServicoRepository.listar_por_cliente(
            cliente_id
        )

    @staticmethod
    def listar_por_veiculo(
        veiculo_id: int,
    ):
        return OrdemServicoRepository.listar_por_veiculo(
            veiculo_id
        )

    @staticmethod
    def excluir(
        ordem_servico: OrdemServico,
    ) -> None:
        OrdemServicoRepository.excluir(
            ordem_servico
        )

    @staticmethod
    def alterar_status(
        ordem_servico: OrdemServico,
        novo_status: str,
    ) -> OrdemServico:
        status_atual = ordem_servico.status

        if novo_status not in {
            OrdemServicoService.STATUS_ABERTA,
            OrdemServicoService.STATUS_EM_ANDAMENTO,
            OrdemServicoService.STATUS_CONCLUIDA,
            OrdemServicoService.STATUS_CANCELADA,
        }:
            raise ValueError("Status de Ordem de Serviço inválido.")

        if novo_status == status_atual:
            raise ValueError("A Ordem de Serviço já possui esse status.")

        status_permitidos = OrdemServicoService.TRANSICOES_PERMITIDAS.get(
            status_atual,
            set(),
        )

        if novo_status not in status_permitidos:
            raise ValueError(
                f"Transição de status não permitida: "
                f"{status_atual} → {novo_status}."
            )

        if (
            novo_status == OrdemServicoService.STATUS_CONCLUIDA
            and not ordem_servico.pagamento_confirmado
        ):
            raise ValueError(
                "A Ordem de Serviço somente pode ser concluída "
                "após a confirmação do pagamento."
            )

        if novo_status == OrdemServicoService.STATUS_CANCELADA:
            if ordem_servico.pagamento_confirmado:
                raise ValueError(
                    "Não é possível cancelar uma Ordem de Serviço "
                    "com pagamento confirmado."
                )

        ordem_servico.status = novo_status

        return ordem_servico

    @staticmethod
    def confirmar_pagamento(
        ordem_servico: OrdemServico,
    ) -> OrdemServico:
        if ordem_servico.pagamento_confirmado:
            raise ValueError(
                "O pagamento desta Ordem de Serviço já foi confirmado."
            )

        if ordem_servico.status == OrdemServicoService.STATUS_CANCELADA:
            raise ValueError(
                "Não é possível confirmar pagamento de uma "
                "Ordem de Serviço cancelada."
            )

        agora = datetime.now(timezone.utc)

        ordem_servico.pagamento_confirmado = True
        ordem_servico.pagamento_confirmado_em = agora

        ordem_servico.veiculo_entregue = True
        ordem_servico.veiculo_entregue_em = agora

        return ordem_servico
