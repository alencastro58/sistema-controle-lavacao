from decimal import Decimal, InvalidOperation

from ..models.movimentacao_fidelidade import MovimentacaoFidelidade
from ..models.programa_fidelidade import ProgramaFidelidade
from ..models.saldo_fidelidade import SaldoFidelidade
from ..repositories.movimentacao_fidelidade_repository import (
    MovimentacaoFidelidadeRepository,
)
from ..repositories.programa_fidelidade_repository import (
    ProgramaFidelidadeRepository,
)
from ..repositories.saldo_fidelidade_repository import (
    SaldoFidelidadeRepository,
)


class ProgramaFidelidadeService:
    TIPO_CREDITO = "CREDITO"
    TIPO_DEBITO = "DEBITO"

    @staticmethod
    def criar(dados: dict) -> ProgramaFidelidade:
        programa = ProgramaFidelidade(
            habilitado=dados.get("habilitado", False),
            pontos_por_real=dados.get("pontos_por_real", 1),
            valor_por_ponto=dados.get("valor_por_ponto", 1),
            desconto_maximo_percentual=dados.get(
                "desconto_maximo_percentual",
                100,
            ),
        )

        return ProgramaFidelidadeRepository.salvar(programa)

    @staticmethod
    def buscar_por_id(
        programa_id: int,
    ) -> ProgramaFidelidade | None:
        return ProgramaFidelidadeRepository.buscar_por_id(
            programa_id
        )

    @staticmethod
    def buscar_primeiro() -> ProgramaFidelidade | None:
        return ProgramaFidelidadeRepository.buscar_primeiro()

    @staticmethod
    def listar_todos() -> list[ProgramaFidelidade]:
        return ProgramaFidelidadeRepository.listar_todos()

    @staticmethod
    def obter_ou_criar_saldo(
        programa: ProgramaFidelidade,
        cliente_id: int,
    ) -> SaldoFidelidade:
        saldo = SaldoFidelidadeRepository.buscar_por_programa_e_cliente(
            programa.id,
            cliente_id,
        )

        if saldo is not None:
            return saldo

        saldo = SaldoFidelidade(
            programa_id=programa.id,
            cliente_id=cliente_id,
            saldo_pontos=0,
            total_acumulado=0,
            total_utilizado=0,
        )

        return SaldoFidelidadeRepository.salvar(saldo)

    @staticmethod
    def creditar_por_ordem_servico(
        ordem_servico,
    ) -> MovimentacaoFidelidade | None:
        programa = ProgramaFidelidadeRepository.buscar_primeiro()

        if programa is None or not programa.habilitado:
            return None

        if ordem_servico.pagamento_confirmado is not True:
            raise ValueError(
                "A OS precisa estar com o pagamento confirmado."
            )

        movimentacao_existente = (
            MovimentacaoFidelidadeRepository.buscar_credito_por_ordem_servico(
                ordem_servico.id
            )
        )

        if movimentacao_existente is not None:
            raise ValueError(
                "Esta Ordem de Serviço já gerou crédito de pontos."
            )

        valor_base = Decimal(
            str(ordem_servico.valor_total or 0)
        )

        if valor_base <= 0:
            return None

        pontos_por_real = Decimal(
            str(programa.pontos_por_real)
        )

        pontos = (
            valor_base * pontos_por_real
        ).quantize(Decimal("0.01"))

        if pontos <= 0:
            return None

        saldo = ProgramaFidelidadeService.obter_ou_criar_saldo(
            programa,
            ordem_servico.cliente_id,
        )

        saldo_anterior = Decimal(
            str(saldo.saldo_pontos)
        )
        saldo_posterior = saldo_anterior + pontos

        saldo.saldo_pontos = saldo_posterior
        saldo.total_acumulado = (
            Decimal(str(saldo.total_acumulado)) + pontos
        )

        movimentacao = MovimentacaoFidelidade(
            programa_id=programa.id,
            cliente_id=ordem_servico.cliente_id,
            saldo_id=saldo.id,
            ordem_servico_id=ordem_servico.id,
            tipo=ProgramaFidelidadeService.TIPO_CREDITO,
            pontos=pontos,
            saldo_anterior=saldo_anterior,
            saldo_posterior=saldo_posterior,
            valor_base=valor_base,
            conversao_pontos=pontos_por_real,
            descricao="Crédito de pontos por pagamento de Ordem de Serviço.",
        )

        return MovimentacaoFidelidadeRepository.salvar(movimentacao)

    @staticmethod
    def debitar_pontos(
        cliente_id: int,
        valor_desconto: Decimal,
        ordem_servico,
    ) -> MovimentacaoFidelidade:
        programa = ProgramaFidelidadeRepository.buscar_primeiro()

        if programa is None or not programa.habilitado:
            raise ValueError(
                "O programa de fidelidade está desabilitado."
            )

        try:
            valor_desconto = Decimal(str(valor_desconto))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError(
                "O valor do desconto deve ser numérico."
            ) from exc

        valor_desconto = valor_desconto.quantize(
            Decimal("0.01")
        )

        if valor_desconto <= 0:
            raise ValueError(
                "O valor do desconto deve ser maior que zero."
            )

        if ordem_servico.cliente_id != cliente_id:
            raise ValueError(
                "O cliente informado não pertence à Ordem de Serviço."
            )

        movimentacoes = (
            MovimentacaoFidelidadeRepository.buscar_por_ordem_servico(
                ordem_servico.id
            )
        )

        if any(
            movimentacao.tipo
            == ProgramaFidelidadeService.TIPO_DEBITO
            for movimentacao in movimentacoes
        ):
            raise ValueError(
                "Esta Ordem de Serviço já utilizou pontos."
            )

        valor_os = Decimal(
            str(ordem_servico.valor_total or 0)
        )

        desconto_atual = Decimal(
            str(ordem_servico.desconto or 0)
        )

        valor_disponivel = valor_os - desconto_atual

        if valor_disponivel <= 0:
            raise ValueError(
                "A Ordem de Serviço não possui valor disponível para desconto."
            )

        if valor_desconto > valor_disponivel:
            raise ValueError(
                "O desconto não pode ultrapassar o valor disponível da OS."
            )

        limite_percentual = Decimal(
            str(programa.desconto_maximo_percentual)
        )

        limite_desconto = (
            valor_os * limite_percentual / Decimal("100")
        ).quantize(Decimal("0.01"))

        if valor_desconto > limite_desconto:
            raise ValueError(
                "O desconto de pontos excede o limite permitido."
            )

        valor_por_ponto = Decimal(
            str(programa.valor_por_ponto)
        )

        if valor_por_ponto <= 0:
            raise ValueError(
                "O valor por ponto deve ser maior que zero."
            )

        pontos_exatos = valor_desconto / valor_por_ponto

        if pontos_exatos != pontos_exatos.to_integral_value():
            raise ValueError(
                "O valor do desconto deve ser múltiplo exato do valor de um ponto."
            )

        pontos = pontos_exatos.to_integral_value()

        saldo = ProgramaFidelidadeService.obter_ou_criar_saldo(
            programa,
            cliente_id,
        )

        saldo_anterior = Decimal(
            str(saldo.saldo_pontos)
        )

        if pontos > saldo_anterior:
            raise ValueError(
                "O cliente não possui saldo de pontos suficiente."
            )

        saldo_posterior = saldo_anterior - pontos

        saldo.saldo_pontos = saldo_posterior
        saldo.total_utilizado = (
            Decimal(str(saldo.total_utilizado)) + pontos
        )

        ordem_servico.desconto = (
            desconto_atual + valor_desconto
        )

        movimentacao = MovimentacaoFidelidade(
            programa_id=programa.id,
            cliente_id=cliente_id,
            saldo_id=saldo.id,
            ordem_servico_id=ordem_servico.id,
            tipo=ProgramaFidelidadeService.TIPO_DEBITO,
            pontos=pontos,
            saldo_anterior=saldo_anterior,
            saldo_posterior=saldo_posterior,
            valor_base=valor_desconto,
            conversao_pontos=valor_por_ponto,
            descricao="Débito de pontos utilizado como desconto.",
        )

        return MovimentacaoFidelidadeRepository.salvar(movimentacao)