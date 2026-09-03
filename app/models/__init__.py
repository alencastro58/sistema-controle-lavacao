from app.models.cliente import Cliente
from app.models.marca import Marca
from app.models.modelo import Modelo
from app.models.porte_veiculo import PorteVeiculo
from app.models.veiculo import Veiculo
from .ordem_servico import OrdemServico
from .servico import Servico
from .item_ordem_servico import ItemOrdemServico
from .lavagem import Lavagem

__all__ = [
    "Cliente",
    "Marca",
    "Modelo",
    "PorteVeiculo",
    "Veiculo",
]