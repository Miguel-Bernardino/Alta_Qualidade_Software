from abc import ABC, abstractmethod

from src.domain.models.cliente import Cliente


class IClienteRepository(ABC):
    @abstractmethod
    def salvar(self, cliente: Cliente) -> None:
        """Persiste um cliente."""
        raise NotImplementedError
