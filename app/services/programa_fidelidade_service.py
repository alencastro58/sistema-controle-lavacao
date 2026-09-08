from ..models.programa_fidelidade import ProgramaFidelidade
from ..repositories.programa_fidelidade_repository import (
    ProgramaFidelidadeRepository,
)


class ProgramaFidelidadeService:
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