from ..models.ordem_servico import OrdemServico
from ..repositories.ordem_servico_repository import OrdemServicoRepository


class OrdemServicoService:
    @staticmethod
    def criar(dados: dict) -> OrdemServico:
        ordem_servico = OrdemServico(
            numero=dados["numero"],
            cliente_id=dados["cliente_id"],
            veiculo_id=dados["veiculo_id"],
            data_agendamento=dados.get("data_agendamento"),
            valor_total=dados.get("valor_total", 0),
            desconto=dados.get("desconto", 0),
            status=dados.get("status", "ABERTA"),
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