from ..models.preco_servico import PrecoServico
from ..repositories.preco_servico_repository import PrecoServicoRepository


class PrecoServicoService:
    @staticmethod
    def criar(dados: dict) -> PrecoServico:
        preco_servico = PrecoServico(
            servico_id=dados["servico_id"],
            porte_id=dados["porte_id"],
            valor=dados["valor"],
            ativo=dados.get("ativo", True),
        )

        return PrecoServicoRepository.salvar(
            preco_servico
        )

    @staticmethod
    def buscar_por_id(
        preco_servico_id: int,
    ) -> PrecoServico | None:
        return PrecoServicoRepository.buscar_por_id(
            preco_servico_id
        )

    @staticmethod
    def listar_todos() -> list[PrecoServico]:
        return PrecoServicoRepository.listar_todos()

    @staticmethod
    def listar_por_servico(
        servico_id: int,
    ) -> list[PrecoServico]:
        return PrecoServicoRepository.listar_por_servico(
            servico_id
        )

    @staticmethod
    def listar_por_porte(
        porte_id: int,
    ) -> list[PrecoServico]:
        return PrecoServicoRepository.listar_por_porte(
            porte_id
        )

    @staticmethod
    def excluir(
        preco_servico: PrecoServico,
    ) -> None:
        PrecoServicoRepository.excluir(
            preco_servico
        )
