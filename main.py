from src.cliente.cliente_concreto import Cliente
from src.cliente.descuento_extra_decorator import DescuentoExtraDecorator
from src.cliente.envio_gratis_decorator import EnvioGratisDecorator
from src.cliente.cashback_decorator import CashbackDecorator
from src.cliente.tipo_cliente import TipoCliente
from src.producto.producto import Producto
from src.pedidos.estado_pedido import EstadoPedido
from src.pedidos.estandar_pedido import EstandarPedido
from src.pedidos.internacional_pedido import InternacionalPedido
from src.pedidos.express_pedido import ExpressPedido
from src.pagos.gestor_metodos_pago import GestorMetodosPago
from src.pagos.pago_tarjeta import PagoTarjeta
from src.pagos.pago_transferencia import PagoTransferencia
from src.pagos.pago_cripto import PagoCripto
from src.pagos.pago_contra_entrega import PagoContraEntrega
from src.factura.factura import Factura
from src.pedidos.gestor_pedido import GestionPedidos

def main():
    # Crear un cliente nuevo de tipo VIP
    cliente = Cliente(
        "Nataniel Palacios",
        "nataniel.palacios@gmail.com",
        "Mozart 1490, Villa Alemana",
        TipoCliente.VIP
    )
    # Decorar el cliente con beneficios temporales
    cliente = DescuentoExtraDecorator(cliente, 0.05)  # +5% descuento extra
    cliente = EnvioGratisDecorator(cliente)            # Envío gratis forzado
    cliente = CashbackDecorator(cliente, 0.03)         # 3% cashback
    # Mostrar información
    print(f"Nombre: {cliente.get_nombre()}")
    print(f"Tipo: {cliente.get_tipo_cliente().value}")
    print(f"Descuento: {cliente.get_descuento() * 100}%")
    print(f"¿Envío gratis?: {cliente.tiene_envio_gratis()}")
    if isinstance(cliente, CashbackDecorator):
        print(f"Cashback: {cliente.get_cashback() * 100}%")
    print()
    
    producto1 = Producto("Chocolate", "123456", 2500, 100)
    producto2 = Producto("Vainilla", "153165", 1500, 200)
    producto3 = Producto("Leche", "983745", 1100, 50)
    
    productos_pedido1 = {
        producto1: 3,  # 3 chocolates
        producto2: 2   # 2 vainillas
    }
    
    productos_pedido2 = {
        producto3: 1   # 1 leche
    }
    
    print("-------------- Descuentos antes del pedido ---------------")
    print(f"Stock de chocolates después del pedido: {producto1.get_stock()}")
    print(f"Stock de vainillas después del pedido: {producto2.get_stock()}")
    print(f"Stock de leche después del pedido: {producto3.get_stock()}")
    print()
    
    gestor_pedidos_singleton = GestionPedidos() # inicializa el Singleton para gestionar pedidos (obtiene la unica instancia de GestionPedidos)

    pedido_estandar = EstandarPedido(100, EstadoPedido.PENDIENTE, productos_pedido1, cliente)
    pedido_int = InternacionalPedido(101, EstadoPedido.PENDIENTE, productos_pedido2, cliente, 25)
    pedido_express = ExpressPedido(102, EstadoPedido.PAGADO, productos_pedido1, cliente, 1000)

    gestor_pedidos_singleton.registrar_pedido(pedido_estandar)
    gestor_pedidos_singleton.registrar_pedido(pedido_int)
    gestor_pedidos_singleton.registrar_pedido(pedido_express)

    gestor_pedidos_singleton.listar_pedidos()

    print("\n")
    
    print("-------------- Cambios de estado de pedido con el singleton ---------------")

    exito_cambio1 = gestor_pedidos_singleton.modificar_estado_pedido(100, EstadoPedido.PAGADO)

    if exito_cambio1:
        print(f"Cambio a {EstadoPedido.PAGADO.value} fue exitoso.")
    else:
        print(f"Cambio a {EstadoPedido.PAGADO.value} falló.")
    print("----------------------------------------------------------------------------")

    pedido_int.descontar_stock_de_productos()
    pedido_estandar.descontar_stock_de_productos()

    print("\n")

    print("-------------- Descuentos despues del pedido ---------------")
    print(f"Stock de chocolates después del pedido: {producto1.get_stock()}")
    print(f"Stock de vainillas después del pedido: {producto2.get_stock()}")
    print(f"Stock de leche después del pedido: {producto3.get_stock()}")
    print()
    
    gestor = GestorMetodosPago()
    gestor.registrar_metodo("tarjeta", PagoTarjeta())
    gestor.registrar_metodo("transferencia", PagoTransferencia())
    gestor.registrar_metodo("cripto", PagoCripto())
    gestor.registrar_metodo("pagoContraEntrega", PagoContraEntrega())
    
    factura1 = Factura(pedido_estandar)
    factura1.imprimir_factura()
    print()
    
    factura1.pagar_factura("tarjeta", gestor)
    print(f"Estado actual del pedido: {pedido_estandar.get_estado().value}")
    print()
    
    factura2 = Factura(pedido_int)
    factura2.imprimir_factura()
    
    print(f"Estado antes de pagar con cripto: {pedido_int.get_estado().value}")
    factura2.pagar_factura("cripto", gestor)
    print(f"Estado despues de pagar con cripto: {pedido_int.get_estado().value}")
    print()
    
    print(f"Estado actual: {pedido_int.get_estado().value}")
    
    # 3. Preparar un envío: PAGADO -> EN_PREPARACION
    prep_exito = pedido_int.cambiar_estado(EstadoPedido.EN_PREPARACION)
    print(f"Preparar envío pedidoInt: {'OK' if prep_exito else 'No válido'}")
    print(f"Estado actual: {pedido_int.get_estado().value}")
    print()
    
    # 4. Enviar un pedido: EN_PREPARACION -> ENVIADO
    envio_exito = pedido_int.cambiar_estado(EstadoPedido.ENVIADO)
    print(f"Enviar pedidoInt: {'OK' if envio_exito else 'No válido'}")
    print(f"Estado actual: {pedido_int.get_estado().value}")
    print()
    
    # 6. Cancelar un pedido: PAGADO -> CANCELADO (solo si no ha sido enviado)
    # Para probar cancelación, necesitamos otro pedido o reiniciar pedidoInt
    pedido_express = ExpressPedido(102, EstadoPedido.PAGADO, productos_pedido1, cliente, 1000)
    cancel_exito = pedido_express.cambiar_estado(EstadoPedido.CANCELADO)
    print(f"Cancelar otroPedido: {'OK' if cancel_exito else 'No válido'}")
    print(f"Estado actual otroPedido: {pedido_express.get_estado().value}")

if __name__ == "__main__":
    main()
