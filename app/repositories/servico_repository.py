from ..extensions import db
from ..models.servico import Servico


class ServicoRepository:
    @staticmethod
    def buscar_por_id(
        servico_id: int,
    ) -> Servico | None:
        return db.session.get(
            Servico,
            servico_id,
        )
