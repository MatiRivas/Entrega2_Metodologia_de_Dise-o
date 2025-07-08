class Producto:
    def __init__(self, nombre, codigo, precio, stock):
        self.nombre = nombre
        self.codigo = codigo
        self.precio = precio
        self.stock = stock
    
    def descontar_stock(self, cantidad):
        if self.stock >= cantidad:
            self.stock -= cantidad
    
    def __eq__(self, other):
        if not isinstance(other, Producto):
            return False
        return self.codigo == other.codigo
    
    def __hash__(self):
        return hash(self.codigo)
    
    def get_nombre(self):
        return self.nombre
    
    def get_precio(self):
        return self.precio
    
    def get_stock(self):
        return self.stock

    def get_codigo(self):
        return self.codigo