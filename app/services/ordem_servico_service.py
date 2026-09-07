from datetime import datetime, timezone
from decimal import Decimal

from ..models.item_ordem_servico import ItemOrdemServico
from ..models.ordem_servico import OrdemServico
from ..repositories.item_ordem_servico_repository import (
    ItemOrdemServicoRepository,
)
from ..repositories.ordem_servico_repository import OrdemServicoRepository
from ..repositories.preco_servico_repository import PrecoServicoRepository
from ..repositories.servico_repository import ServicoRepository
from ..repositories.veiculo_repository import VeiculoRepository


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
        itens_dados = dados.get("itens", [])

        # Compatibilidade com o fluxo legado:
        # uma OS pode ser criada inicialmente sem itens.
        # Nesse caso, os valores informados são preservados.
        if not itens_dados:
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

            return OrdemServicoRepository.salvar(ordem_servico)

        veiculo = VeiculoRepository.buscar_por_id(
            dados["veiculo_id"]
        )

        if veiculo is None:
            raise ValueError("Veículo não encontrado.")

        if veiculo.cliente_id != dados["cliente_id"]:
            raise ValueError(
                "O veículo informado não pertence ao cliente."
            )

        ordem_servico = OrdemServico(
            numero=dados["numero"],
            cliente_id=dados["cliente_id"],
            veiculo_id=dados["veiculo_id"],
            data_agendamento=dados.get("data_agendamento"),
            valor_total=0,
            desconto=0,
            status=OrdemServicoService.STATUS_ABERTA,
            observacoes=dados.get("observacoes"),
        )

        OrdemServicoRepository.salvar(ordem_servico)

        OrdemServicoService._recalcular_itens(
            ordem_servico,
            itens_dados,
            dados.get("desconto", 0),
        )

        return ordem_servico

    @staticmethod
    def editar(
        ordem_servico: OrdemServico,
        dados: dict,
    ) -> OrdemServico:
        if ordem_servico.status in {
            OrdemServicoService.STATUS_CONCLUIDA,
            OrdemServicoService.STATUS_CANCELADA,
        }:
            raise ValueError(
                "Não é possível editar uma Ordem de Serviço "
                "concluída ou cancelada."
            )

        if ordem_servico.pagamento_confirmado:
            campos_protegidos = {
                "cliente_id",
                "veiculo_id",
            }

            if any(
                campo in dados
                and dados[campo] != getattr(
                    ordem_servico,
                    campo,
                )
                for campo in campos_protegidos
            ):
                raise ValueError(
                    "Não é possível alterar cliente ou veículo "
                    "após a confirmação do pagamento."
                )

        cliente_id = dados.get(
            "cliente_id",
            ordem_servico.cliente_id,
        )

        veiculo_id = dados.get(
            "veiculo_id",
            ordem_servico.veiculo_id,
        )

        veiculo = VeiculoRepository.buscar_por_id(veiculo_id)

        if veiculo is None:
            raise ValueError("Veículo não encontrado.")

        if veiculo.cliente_id != cliente_id:
            raise ValueError(
                "O veículo informado não pertence ao cliente."
            )

        if "numero" in dados:
            ordem_servico.numero = dados["numero"]

        ordem_servico.cliente_id = cliente_id
        ordem_servico.veiculo_id = veiculo_id

        if "data_agendamento" in dados:
            ordem_servico.data_agendamento = (
                dados["data_agendamento"]
            )

        if "observacoes" in dados:
            ordem_servico.observacoes = dados["observacoes"]

        itens_dados = dados.get("itens")

        if itens_dados is not None:
            desconto_ordem = dados.get(
                "desconto",
                0,
            )

            OrdemServicoService._recalcular_itens(
                ordem_servico,
                itens_dados,
                desconto_ordem,
            )
        elif "desconto" in dados:
            desconto_atual = Decimal(
                str(ordem_servico.desconto or 0)
            )

            valor_total_atual = Decimal(
                str(ordem_servico.valor_total or 0)
            )

            novo_desconto = Decimal(
                str(dados["desconto"])
            )

            if novo_desconto < 0:
                raise ValueError(
                    "O desconto da Ordem de Serviço "
                    "não pode ser negativo."
                )

            desconto_itens = (
                desconto_atual
                - Decimal(
                    str(
                        sum(
                            Decimal(str(item.desconto or 0))
                            for item in ordem_servico.itens
                        )
                    )
                )
            )

            novo_valor_total = (
                valor_total_atual
                + desconto_atual
                - desconto_itens
                - novo_desconto
            )

            if novo_valor_total < 0:
                raise ValueError(
                    "O desconto não pode ser maior "
                    "que o valor da Ordem de Serviço."
                )

            ordem_servico.desconto = (
                desconto_itens + novo_desconto
            )

            ordem_servico.valor_total = novo_valor_total

        return ordem_servico

    @staticmethod
    def _recalcular_itens(
        ordem_servico: OrdemServico,
        itens_dados: list[dict],
        desconto_ordem,
    ) -> None:
        veiculo = VeiculoRepository.buscar_por_id(
            ordem_servico.veiculo_id
        )

        if veiculo is None:
            raise ValueError("Veículo não encontrado.")

        for item in list(ordem_servico.itens):
            ItemOrdemServicoRepository.excluir(item)

        subtotal = Decimal("0.00")
        desconto_itens = Decimal("0.00")

        for item_dados in itens_dados:
            servico_id = item_dados["servico_id"]

            servico = ServicoRepository.buscar_por_id(
                servico_id
            )

            if servico is None:
                raise ValueError(
                    f"Serviço não encontrado: {servico_id}."
                )

            if not servico.ativo:
                raise ValueError(
                    f"O serviço '{servico.nome}' está inativo."
                )

            preco = (
                PrecoServicoRepository.buscar_por_servico_e_porte(
                    servico_id,
                    veiculo.porte_id,
                )
            )

            if preco is None:
                raise ValueError(
                    f"Não existe preço ativo para o serviço "
                    f"'{servico.nome}' no porte do veículo."
                )

            quantidade = item_dados.get("quantidade", 1)

            desconto = item_dados.get("desconto", 0)

            tipo_desconto = item_dados.get(
                "tipo_desconto",
                "NENHUM",
            )

            item = ItemOrdemServico(
                ordem_servico_id=ordem_servico.id,
                servico_id=servico.id,
                quantidade=quantidade,
                valor_unitario=preco.valor,
                desconto=desconto,
                tipo_desconto=tipo_desconto,
            )

            ItemOrdemServicoRepository.salvar(item)

            subtotal += Decimal(str(item.valor_bruto))
            desconto_itens += Decimal(str(item.desconto))

        desconto_ordem = Decimal(
            str(desconto_ordem)
        )

        if desconto_ordem < 0:
            raise ValueError(
                "O desconto da Ordem de Serviço "
                "não pode ser negativo."
            )

        valor_total = (
            subtotal
            - desconto_itens
            - desconto_ordem
        )

        if valor_total < 0:
            raise ValueError(
                "O desconto não pode ser maior "
                "que o valor da Ordem de Serviço."
            )

        ordem_servico.desconto = (
            desconto_itens + desconto_ordem
        )

        ordem_servico.valor_total = valor_total

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