from typing import Dict, List, Optional
from src.producto.producto import Producto
from api.modelos.schemas import ProductoRequest, ProductoResponse

class ProductoService:
    """Servicio para gestionar operaciones de productos"""
    
    def __init__(self):
        self.productos_db: Dict[str, Producto] = {}
    
    def crear_producto(self, producto_request: ProductoRequest) -> ProductoResponse:
        """Crea un nuevo producto en el sistema"""
        if producto_request.codigo in self.productos_db:
            raise ValueError(f"Producto con código {producto_request.codigo} ya existe")
        
        producto = Producto(
            producto_request.nombre,
            producto_request.codigo,
            producto_request.precio,
            producto_request.stock
        )
        
        self.productos_db[producto_request.codigo] = producto
        
        return ProductoResponse(
            codigo=producto.get_codigo(),
            nombre=producto.get_nombre(),
            precio=producto.get_precio(),
            stock=producto.get_stock()
        )
    
    def obtener_producto(self, codigo: str) -> Optional[Producto]:
        """Obtiene un producto por su código"""
        return self.productos_db.get(codigo)
    
    def listar_productos(self) -> List[ProductoResponse]:
        """Lista todos los productos del sistema"""
        productos = []
        for codigo, producto in self.productos_db.items():
            productos.append(ProductoResponse(
                codigo=producto.get_codigo(),
                nombre=producto.get_nombre(),
                precio=producto.get_precio(),
                stock=producto.get_stock()
            ))
        return productos
    
    def producto_existe(self, codigo: str) -> bool:
        """Verifica si un producto existe en el sistema"""
        return codigo in self.productos_db
