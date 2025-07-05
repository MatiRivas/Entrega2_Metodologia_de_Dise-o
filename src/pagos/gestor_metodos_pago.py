class GestorMetodosPago:
    def __init__(self):
        self.metodos_pago = {}
    
    def registrar_metodo(self, nombre, metodo):
        self.metodos_pago[nombre.lower()] = metodo
    
    def eliminar_metodo(self, nombre):
        if nombre.lower() in self.metodos_pago:
            del self.metodos_pago[nombre.lower()]
    
    def obtener_metodo(self, nombre):
        return self.metodos_pago.get(nombre.lower())
    
    def existe_metodo(self, nombre):
        return nombre.lower() in self.metodos_pago
