from typing import Dict, List, Optional
from src.cliente.cliente_concreto import Cliente
from src.cliente.tipo_cliente import TipoCliente
from api.modelos.schemas import ClienteRequest, ClienteResponse

class ClienteService:
    """Servicio para gestionar operaciones de clientes"""
    
    def __init__(self):
        self.clientes_db: Dict[str, Cliente] = {}
    
    def crear_cliente(self, cliente_request: ClienteRequest) -> ClienteResponse:
        """Crea un nuevo cliente en el sistema"""
        if cliente_request.email in self.clientes_db:
            raise ValueError(f"Cliente con email {cliente_request.email} ya existe")
        
        tipo_cliente = TipoCliente(cliente_request.tipo_cliente)
        cliente = Cliente(
            cliente_request.nombre,
            cliente_request.email,
            cliente_request.direccion,
            tipo_cliente
        )
        
        self.clientes_db[cliente_request.email] = cliente
        
        return ClienteResponse(
            email=cliente.get_email(),
            nombre=cliente.get_nombre(),
            tipo=cliente.get_tipo_cliente().value,
            descuento=cliente.get_descuento(),
            direccion=cliente.get_direccion()
        )
    
    def obtener_cliente(self, email: str) -> Optional[Cliente]:
        """Obtiene un cliente por su email"""
        return self.clientes_db.get(email)
    
    def listar_clientes(self) -> List[ClienteResponse]:
        """Lista todos los clientes del sistema"""
        clientes = []
        for email, cliente in self.clientes_db.items():
            clientes.append(ClienteResponse(
                email=cliente.get_email(),
                nombre=cliente.get_nombre(),
                tipo=cliente.get_tipo_cliente().value,
                descuento=cliente.get_descuento(),
                direccion=cliente.get_direccion()
            ))
        return clientes
    
    def cliente_existe(self, email: str) -> bool:
        """Verifica si un cliente existe en el sistema"""
        return email in self.clientes_db
