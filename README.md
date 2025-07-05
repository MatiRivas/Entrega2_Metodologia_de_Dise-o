# Entrega2_MDD - Sistema de Gestión de Pedidos

Este proyecto implementa un sistema de gestión de pedidos modularizado siguiendo una estructura similar a Java.

## Estructura del Proyecto

```
Entrega2_MDD/
├── src/
│   ├── cliente/
│   │   ├── __init__.py
│   │   ├── tipo_cliente.py      # Enum TipoCliente
│   │   └── cliente.py           # Clase Cliente
│   ├── producto/
│   │   ├── __init__.py
│   │   └── producto.py          # Clase Producto
│   ├── pedidos/
│   │   ├── __init__.py
│   │   ├── estado_pedido.py     # Enum EstadoPedido
│   │   ├── pedido.py            # Clase abstracta Pedido
│   │   ├── estandar_pedido.py   # EstandarPedido
│   │   ├── pedido_con_cobro.py  # Clase abstracta PedidoConCobro
│   │   ├── pedido_cambio_fecha.py # Clase abstracta PedidoCambioFecha
│   │   ├── internacional_pedido.py # InternacionalPedido
│   │   ├── express_pedido.py    # ExpressPedido
│   │   └── programado_pedido.py # ProgramadoPedido
│   ├── pagos/
│   │   ├── __init__.py
│   │   ├── metodo_pago.py       # Interfaz MetodoPago
│   │   ├── pago_tarjeta.py      # PagoTarjeta
│   │   ├── pago_transferencia.py # PagoTransferencia
│   │   ├── pago_cripto.py       # PagoCripto
│   │   ├── pago_contra_entrega.py # PagoContraEntrega
│   │   └── gestor_metodos_pago.py # GestorMetodosPago
│   └── factura/
│       ├── __init__.py
│       └── factura.py           # Clase Factura
├── main.py                      # Archivo principal con ejemplos
└── README.md
```

## Descripción de las Clases

### Cliente
- **TipoCliente**: Enum que define los tipos de cliente (NUEVO, FRECUENTE, VIP)
- **Cliente**: Gestiona la información del cliente y sus beneficios

### Producto
- **Producto**: Representa un producto con nombre, código, precio y stock

### Pedidos
- **EstadoPedido**: Enum que define los estados del pedido
- **Pedido**: Clase abstracta base para todos los tipos de pedidos
- **EstandarPedido**: Pedido básico sin características especiales
- **PedidoConCobro**: Clase abstracta para pedidos con cobros adicionales
- **PedidoCambioFecha**: Clase abstracta para pedidos que permiten cambio de fecha
- **InternacionalPedido**: Pedido con impuestos aduaneros
- **ExpressPedido**: Pedido con cargo extra por entrega rápida
- **ProgramadoPedido**: Pedido con fecha de entrega programada

### Pagos
- **MetodoPago**: Interfaz abstracta para métodos de pago
- **PagoTarjeta**: Pago con tarjeta de crédito/débito
- **PagoTransferencia**: Pago por transferencia bancaria
- **PagoCripto**: Pago con criptomonedas
- **PagoContraEntrega**: Pago al momento de la entrega
- **GestorMetodosPago**: Gestor para registrar y administrar métodos de pago

### Factura
- **Factura**: Maneja la facturación, cálculo de totales y procesamiento de pagos

## Cómo ejecutar

```bash
python main.py
```

## Características implementadas

1. **Gestión de Clientes**: Diferentes tipos de clientes con descuentos específicos
2. **Gestión de Productos**: Control de stock y precios
3. **Estados de Pedidos**: Transiciones válidas entre estados
4. **Múltiples tipos de Pedidos**: Estándar, Internacional, Express, Programado
5. **Sistemas de Pago**: Múltiples métodos de pago intercambiables
6. **Facturación**: Cálculo automático de totales, descuentos e impuestos
7. **Modularización**: Estructura organizada en paquetes y módulos
