from src.cliente.cliente_concreto import Cliente
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
from src.pagos.proxy_pago import ProxyPago
from src.factura.factura import Factura
from src.pedidos.gestor_pedido import GestionPedidos

from src.pagos.pago_QR import PagoQR
from src.pagos.proxy_pagoQR import ProxyPagoQR
from src.auditoria.registro_transacciones import RegistroTransacciones
from src.seguridad.gestor_tokens_temporales import GestorTokensTemporales
import time

def main():
    # Crear un cliente nuevo de tipo VIP
    cliente = Cliente(
        "Nataniel Palacios",
        "nataniel.palacios@gmail.com",
        "Mozart 1490, Villa Alemana",
        TipoCliente.VIP
    )
    
    # Mostrar información
    print(f"Nombre: {cliente.get_nombre()}")
    print(f"Email: {cliente.get_email()}")
    print(f"Dirección: {cliente.get_direccion()}")  
    print(f"Tipo: {cliente.get_tipo_cliente().value}")
    print(f"Descuento: {cliente.get_descuento() * 100}%")
    print(f"¿Envío gratis?: {cliente.tiene_envio_gratis()}")
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

    # Usar ProxyPago para validaciones antes de pagar
    metodo_tarjeta = gestor.obtener_metodo("tarjeta")
    proxy_tarjeta = ProxyPago(metodo_tarjeta, cliente)
    monto1 = factura1.get_monto_final()
    exito_pago1 = proxy_tarjeta.procesar_pago(monto1)
    if exito_pago1:
        pedido_estandar.cambiar_estado(EstadoPedido.PAGADO)
    print(f"Estado actual del pedido: {pedido_estandar.get_estado().value}")
    print()

    factura2 = Factura(pedido_int)
    factura2.imprimir_factura()

    print(f"Estado antes de pagar con cripto: {pedido_int.get_estado().value}")
    metodo_cripto = gestor.obtener_metodo("cripto")
    proxy_cripto = ProxyPago(metodo_cripto, cliente)
    monto2 = factura2.get_monto_final()
    # Aplicar todas las verificaciones explícitamente antes de procesar el pago
    if proxy_cripto.verificar_datos_cliente() and proxy_cripto.control_fraude(monto2):
        proxy_cripto.registrar_auditoria(monto2)
        exito_pago2 = proxy_cripto.procesar_pago(monto2)
        if exito_pago2:
            pedido_int.cambiar_estado(EstadoPedido.PAGADO)
    else:
        print("No se pudo procesar el pago por fallas en las verificaciones.")
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

    # --- INICIO DE LA DEMOSTRACIÓN DE PAGO QR CON EL NUEVO PROXY ---
    print("\n\n--- INICIANDO DEMOSTRACIÓN DE PAGO QR CON PROXY ESPECÍFICO ---")

    # 1. Instancias de las nuevas dependencias
    registro_transacciones_qr = RegistroTransacciones(archivo_log="log_uvshop_transacciones_qr.log")
    gestor_tokens_qr = GestorTokensTemporales()
    
    # 2. Cliente y Producto para la demo QR
    cliente_qr = Cliente("Alice QR", "alice.qr@example.com", "Av. Siempre Viva 742", TipoCliente.FRECUENTE)
    producto_qr_ejemplo = Producto("Cargador Universal QR", "QRDEV001", 350.00, 50)
    producto_qr_bajo = Producto("Cable USB-C", "QRACC002", 80.00, 100) # Para probar monto bajo

    # 3. Pedido para el pago QR
    pedido_qr_exitoso = EstandarPedido(300, EstadoPedido.PENDIENTE, {producto_qr_ejemplo: 1}, cliente_qr)
    factura_qr_exitoso = Factura(pedido_qr_exitoso)
    monto_qr_exitoso = factura_qr_exitoso.get_monto_final()

    pedido_qr_fallo_monto = EstandarPedido(301, EstadoPedido.PENDIENTE, {producto_qr_bajo: 1}, cliente_qr)
    factura_qr_fallo_monto = Factura(pedido_qr_fallo_monto)
    monto_qr_fallo_monto = factura_qr_fallo_monto.get_monto_final()


    # 4. Instancia del Sujeto Real (PagoCodigoQR)
    pago_qr_real_instance = PagoQR()

    # 5. Instancia del Proxy Específico para QR
    proxy_pago_qr_instance = ProxyPagoQR(
        metodo_pago_real=pago_qr_real_instance,
        registro=registro_transacciones_qr,
        gestor_tokens=gestor_tokens_qr
    )

    # 6. Registrar el nuevo método de pago (el proxy) en el gestor de pagos
    gestor.registrar_metodo("codigo_qr", proxy_pago_qr_instance)


    # --- CASO DE PRUEBA 1: Pago QR Exitoso ---
    print("\n--- TEST: Pago QR Exitoso ---")
    print(f"Estado inicial del Pedido {pedido_qr_exitoso.get_id()}: {pedido_qr_exitoso.get_estado().value}")
    
    # Simular la generación y obtención del token por parte del frontend/cliente
    token_para_alice = gestor_tokens_qr.generar_token(cliente_qr.get_email())
    
    print("\n[DEMO QR] Intentando procesar pago QR con token válido...")
    # Llamamos al método procesar_pago del proxy, pasándole el cliente y el token
    # El gestor de pagos lo hará por nosotros si se lo pides, o puedes llamarlo directo para la demo
    pago_qr_ok = proxy_pago_qr_instance.procesar_pago(monto_qr_exitoso, cliente=cliente_qr, token_temporal=token_para_alice)

    if pago_qr_ok:
        pedido_qr_exitoso.cambiar_estado(EstadoPedido.PAGADO)
        print(f"[DEMO QR] Pago QR de ${monto_qr_exitoso} exitoso para {cliente_qr.get_email()}.")
    else:
        print(f"[DEMO QR] Pago QR de ${monto_qr_exitoso} fallido para {cliente_qr.get_email()}.")
    print(f"Estado final del Pedido {pedido_qr_exitoso.get_id()}: {pedido_qr_exitoso.get_estado().value}")


    # --- CASO DE PRUEBA 2: Pago QR Fallido por Token Expirado ---
    print("\n--- TEST: Pago QR Fallido por Token Expirado ---")
    print(f"Estado inicial del Pedido {pedido_qr_fallo_monto.get_id()}: {pedido_qr_fallo_monto.get_estado().value}")

    token_para_expirar = gestor_tokens_qr.generar_token(cliente_qr.get_email())
    print(f"[DEMO QR] Generado token para expirar: {token_para_expirar}. Esperando {gestor_tokens_qr.TOKEN_EXPIRATION_MINUTES + 1} minutos...")
    time.sleep((gestor_tokens_qr.TOKEN_EXPIRATION_MINUTES + 1) * 60) # Espera para que el token expire
    
    print("\n[DEMO QR] Intentando procesar pago QR con token expirado...")
    pago_qr_fallo_exp = proxy_pago_qr_instance.procesar_pago(monto_qr_exitoso, cliente=cliente_qr, token_temporal=token_para_expirar)

    if not pago_qr_fallo_exp:
        print(f"[DEMO QR] Pago QR fallido por token expirado (como se esperaba).")
    else:
        print(f"[DEMO QR] ERROR: Pago QR con token expirado ¡no falló!")
    print(f"Estado final del Pedido {pedido_qr_fallo_monto.get_id()}: {pedido_qr_fallo_monto.get_estado().value}")


    # --- CASO DE PRUEBA 3: Pago QR Fallido por Monto Demasiado Bajo (rechazo de pasarela real) ---
    print("\n--- TEST: Pago QR Fallido por Monto Demasiado Bajo ---")
    print(f"Estado inicial del Pedido {pedido_qr_fallo_monto.get_id()}: {pedido_qr_fallo_monto.get_estado().value}")
    
    token_para_bob = gestor_tokens_qr.generar_token(cliente_qr.get_email()) # Usa el mismo cliente para simplificar
    
    print(f"\n[DEMO QR] Intentando procesar pago QR de ${monto_qr_fallo_monto} (monto bajo) con token válido...")
    pago_qr_fallo_monto_bajo = proxy_pago_qr_instance.procesar_pago(monto_qr_fallo_monto, cliente=cliente_qr, token_temporal=token_para_bob)

    if not pago_qr_fallo_monto_bajo:
        print(f"[DEMO QR] Pago QR fallido por monto bajo (rechazado por la pasarela real - como se esperaba).")
    else:
        print(f"[DEMO QR] ERROR: Pago QR con monto bajo ¡no falló!")
    print(f"Estado final del Pedido {pedido_qr_fallo_monto.get_id()}: {pedido_qr_fallo_monto.get_estado().value}")


    print("\n--- FIN DEMOSTRACIÓN DE PAGO QR ---")


if __name__ == "__main__":
    main()
