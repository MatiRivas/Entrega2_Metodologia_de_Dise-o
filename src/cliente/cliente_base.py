from abc import ABC, abstractmethod

class ClienteBase(ABC):
    @abstractmethod
    def get_descuento(self):
        pass
    @abstractmethod
    def tiene_envio_gratis(self):
        pass
    @abstractmethod
    def get_nombre(self):
        pass
    @abstractmethod
    def get_tipo_cliente(self):
        pass
    @abstractmethod
    def get_direccion(self):
        pass
