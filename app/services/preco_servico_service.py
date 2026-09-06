from app.models.preco_servico import PrecoServico
from app.repositories.preco_servico_repository import (
    PrecoServicoRepository,
)


class PrecoServicoService:

    @staticmethod
    def criar(dados):
        preco_servico = PrecoServico(
            servico_id=dados["servico_id"],
            porte_id=dados["porte_id"],
            valor=dados["valor"],
            ativo=dados.get("ativo", True),
        )

        return PrecoServicoRepository.salvar(preco_servico)

    @staticmethod
    def buscar_por_id(preco_servico_id):
        return PrecoServicoRepository.buscar_por_id(
            preco_servico_id
        )

    @staticmethod
    def listar_todos():
        return PrecoServicoRepository.listar_todos()

    @staticmethod
    def listar_por_servico(servico_id):
        return PrecoServicoRepository.listar_por_servico(
            servico_id
        )

    @staticmethod
    def listar_por_porte(porte_id):
        return PrecoServicoRepository.listar_por_porte(
            porte_id
        )

    @staticmethod
    def excluir(preco_servico):
        if isinstance(preco_servico, int):
            preco_servico = (
                PrecoServicoRepository.buscar_por_id(
                    preco_servico
                )
            )

            if preco_servico is None:
                raise ValueError(
                    "Preço de serviço não encontrado."
                )

        if not isinstance(preco_servico, PrecoServico):
            raise TypeError(
                "O preço de serviço deve ser uma instância "
                "de PrecoServico ou um ID inteiro."
            )

        PrecoServicoRepository.excluir(preco_servico)