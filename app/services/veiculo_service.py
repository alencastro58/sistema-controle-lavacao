from ..models.veiculo import Veiculo
from ..repositories.veiculo_repository import VeiculoRepository


class VeiculoService:
    @staticmethod
    def criar(dados: dict) -> Veiculo:
        veiculo = Veiculo(
            cliente_id=dados["cliente_id"],
            modelo_id=dados["modelo_id"],
            porte_id=dados["porte_id"],
            placa=dados["placa"],
            cor=dados["cor"],
            ano_fabricacao=dados.get("ano_fabricacao"),
            ano_modelo=dados.get("ano_modelo"),
            renavam=dados.get("renavam"),
            chassi=dados.get("chassi"),
            observacoes=dados.get("observacoes"),
        )

        return VeiculoRepository.salvar(veiculo)

    @staticmethod
    def buscar_por_id(veiculo_id: int) -> Veiculo | None:
        return VeiculoRepository.buscar_por_id(veiculo_id)

    @staticmethod
    def buscar_por_placa(placa: str) -> Veiculo | None:
        return VeiculoRepository.buscar_por_placa(placa)

    @staticmethod
    def listar_todos() -> list[Veiculo]:
        return VeiculoRepository.listar_todos()

    @staticmethod
    def listar_ativos() -> list[Veiculo]:
        return VeiculoRepository.listar_ativos()

    @staticmethod
    def listar_por_cliente(
        cliente_id: int,
    ) -> list[Veiculo]:
        return VeiculoRepository.listar_por_cliente(cliente_id)

    @staticmethod
    def excluir(veiculo: Veiculo) -> None:
        VeiculoRepository.excluir(veiculo)