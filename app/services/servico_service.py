from ..repositories.servico_repository import ServicoRepository


class ServicoService:
    @staticmethod
    def buscar_por_id(
        servico_id: int,
    ):
        return ServicoRepository.buscar_por_id(
            servico_id,
        )
