from ..models.cliente import Cliente
from ..repositories.cliente_repository import ClienteRepository


class ClienteService:
    @staticmethod
    def criar(dados: dict) -> Cliente:
        cliente = Cliente(
            tipo_pessoa=dados["tipo_pessoa"],
            nome_razao_social=dados["nome_razao_social"],
            nome_fantasia=dados.get("nome_fantasia"),
            cpf_cnpj=dados.get("cpf_cnpj"),
            email=dados["email"],
            telefone=dados["telefone"],
            data_nascimento=dados.get("data_nascimento"),
            inscricao_estadual=dados.get("inscricao_estadual"),
            cep=dados.get("cep"),
            logradouro=dados.get("logradouro"),
            numero=dados.get("numero"),
            complemento=dados.get("complemento"),
            bairro=dados.get("bairro"),
            cidade=dados.get("cidade"),
            uf=dados.get("uf"),
        )

        return ClienteRepository.salvar(cliente)

    @staticmethod
    def buscar_por_id(cliente_id: int) -> Cliente | None:
        return ClienteRepository.buscar_por_id(cliente_id)

    @staticmethod
    def buscar_por_cpf_cnpj(cpf_cnpj: str) -> Cliente | None:
        return ClienteRepository.buscar_por_cpf_cnpj(cpf_cnpj)

    @staticmethod
    def listar_todos() -> list[Cliente]:
        return ClienteRepository.listar_todos()

    @staticmethod
    def listar_ativos() -> list[Cliente]:
        return ClienteRepository.listar_ativos()

    @staticmethod
    def excluir(cliente: Cliente) -> None:
        ClienteRepository.excluir(cliente)