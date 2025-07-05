from .pedido import Pedido

class GestionPedidos:
    _instancia = None
    _todos_los_pedidos = {} # Aquí se guardarían todos los pedidos (estandar, internacional, etc.)

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def registrar_pedido(self, pedido):
        # Lógica para añadir un pedido (sea Estandar, Internacional, etc.)
        self._todos_los_pedidos[pedido.get_id()] = pedido
        print(f"Pedido {pedido.get_id()} registrado.")

    def consultar_pedido(self, id_pedido):
        # Lógica para obtener un pedido específico
        return self._todos_los_pedidos.get(id_pedido)
    
    def listar_pedidos(self):
        """Lista todos los pedidos registrados."""
        if not self._todos_los_pedidos:
            print("No hay pedidos registrados en el sistema.")
            return
        print("\n--- Listado de Pedidos ---")
        for id_pedido, pedido in self._todos_los_pedidos.items():
            cliente_nombre = pedido.get_cliente().get_nombre() if pedido.get_cliente() else "Desconocido"
            print(f"ID: {id_pedido}, Estado: {pedido.get_estado().value}, Cliente: {cliente_nombre}")
        
    
    def modificar_estado_pedido(self, id_pedido, nuevo_estado): #asumimos que solo cambiaremos el estado en este caso
        """Actualiza el estado de un pedido específico a través del gestor."""
        pedido = self.consultar_pedido(id_pedido)
        if pedido:
            return pedido.cambiar_estado(nuevo_estado)
        else:
            print(f"Error: Pedido con ID {id_pedido} no encontrado para actualizar estado.")
            return False