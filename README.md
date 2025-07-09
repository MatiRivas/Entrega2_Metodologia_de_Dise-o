# Entrega2_MDD - Sistema de Gestión de Pedidos

Este proyecto implementa un sistema de gestión de pedidos modularizado siguiendo una estructura similar a Java, con una **API REST construida con FastAPI** utilizando arquitectura **MVC**.

## 🚀 Características Principales

- ✅ **Arquitectura MVC**: Separación clara entre Modelo, Vista y Controlador
- ✅ **API REST**: Endpoints RESTful con FastAPI
- ✅ **Pago QR**: Sistema de pagos QR con autenticación por tokens
- ✅ **Patrones de Diseño**: Proxy, Strategy, Factory, Decorator
- ✅ **Logging**: Registro automático de transacciones
- ✅ **Validación**: Validación automática con Pydantic
- ✅ **Documentación**: Swagger UI automática

## 🏗️ Estructura del Proyecto

```
Entrega2_MDD/
├── app.py                       # Punto de entrada FastAPI
├── src/                         # Dominio de la aplicación
│   ├── cliente/
│   │   ├── cliente_base.py
│   │   ├── cliente_concreto.py
│   │   ├── cliente_decorator.py
│   │   ├── cashback_decorator.py
│   │   ├── descuento_extra_decorator.py
│   │   ├── envio_gratis_decorator.py
│   │   └── tipo_cliente.py
│   ├── producto/
│   │   └── producto.py
│   ├── pedidos/
│   │   ├── estado_pedido.py
│   │   ├── pedido.py
│   │   ├── estandar_pedido.py
│   │   ├── express_pedido.py
│   │   ├── internacional_pedido.py
│   │   ├── programado_pedido.py
│   │   └── gestor_pedido.py
│   ├── pagos/
│   │   ├── metodo_pago.py
│   │   ├── pago_tarjeta.py
│   │   ├── pago_transferencia.py
│   │   ├── pago_cripto.py
│   │   ├── pago_contra_entrega.py
│   │   ├── pago_QR.py
│   │   ├── proxy_pagoQR.py      # 🆕 Proxy para pago QR
│   │   └── gestor_metodos_pago.py
│   ├── factura/
│   │   └── factura.py
│   ├── auditoria/
│   │   └── registro_transacciones.py
│   └── seguridad/
│       └── gestor_tokens_temporales.py
├── api/                         # 🆕 Capa MVC
│   ├── modelos/
│   │   └── schemas.py           # DTOs/Schemas de Pydantic
│   ├── servicios/
│   │   ├── cliente_service.py   # Lógica de negocio - Clientes
│   │   ├── producto_service.py  # Lógica de negocio - Productos
│   │   ├── token_service.py     # Lógica de negocio - Tokens
│   │   └── pago_service.py      # Lógica de negocio - Pagos
│   ├── controladores/
│   │   ├── cliente_controller.py    # Endpoints - Clientes
│   │   ├── producto_controller.py   # Endpoints - Productos
│   │   ├── token_controller.py      # Endpoints - Tokens
│   │   ├── pago_controller.py       # Endpoints - Pagos
│   │   ├── health_controller.py     # Endpoints - Health
│   │   └── main_router.py           # Router principal
│   └── dependencies.py          # Gestión de dependencias
└── main.py                      # Archivo con ejemplos del dominio
```

## 🛠️ Instalación y Configuración

### Requisitos
```bash
pip install fastapi uvicorn pydantic
```

### Ejecutar la aplicación

#### **Opción 1: Servidor API REST (Recomendado)**
```bash
# Usando Uvicorn
python -m uvicorn app:app --reload --port 8000

# O ejecutando app.py directamente
python app.py
```

#### **Opción 2: Ejemplos del dominio**
```bash
# Solo para probar las clases del dominio sin API
python main.py
```

### Acceder a la aplicación
```bash
# Documentación interactiva Swagger
http://localhost:8000/docs

# Documentación ReDoc
http://localhost:8000/redoc

# Endpoint de prueba
http://localhost:8000/
```

## 📚 Documentación Adicional

- **[ARQUITECTURA_MVC.md](ARQUITECTURA_MVC.md)**: Descripción detallada de la arquitectura MVC
- **[EJEMPLOS_USO.md](EJEMPLOS_USO.md)**: Ejemplos prácticos de uso de la API

## 🔗 Endpoints Principales

### Clientes
- `POST /clientes/` - Crear cliente
- `GET /clientes/` - Listar clientes
- `GET /clientes/{email}` - Obtener cliente

### Productos
- `POST /productos/` - Crear producto
- `GET /productos/` - Listar productos
- `GET /productos/{codigo}` - Obtener producto

### Tokens
- `POST /tokens/generar` - Generar token QR
- `POST /tokens/validar` - Validar token

### Pagos
- `POST /pagos/procesar` - Procesar pago
- `GET /pagos/metodos` - Métodos disponibles

### Health Check
- `GET /health/` - Estado del sistema

## 🎯 Características del Sistema de Pagos QR

1. **Autenticación por Token**: Cada pago QR requiere un token temporal
2. **Validación de Seguridad**: Tokens con expiración automática
3. **Logging Automático**: Registro de todas las transacciones QR
4. **Patrón Proxy**: Intercepta y valida pagos QR sin modificar el código original

## 📋 Ejemplo de Uso Rápido

```bash
# 1. Crear cliente
curl -X POST "http://localhost:8000/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@email.com",
    "direccion": "Calle 123",
    "tipo_cliente": "VIP"
  }'

# 2. Generar token QR
curl -X POST "http://localhost:8000/tokens/generar" \
  -H "Content-Type: application/json" \
  -d '{"cliente_email": "juan@email.com"}'

# 3. Procesar pago QR
curl -X POST "http://localhost:8000/pagos/procesar" \
  -H "Content-Type: application/json" \
  -d '{
    "pedido_id": 1,
    "metodo_pago": "qr",
    "monto": 100.00,
    "cliente_email": "juan@email.com",
    "token_temporal": "[TOKEN_OBTENIDO]"
  }'
```

## 🏛️ Arquitectura MVC Implementada

### **Modelo (api/modelos/)**
- Schemas de Pydantic para validación
- DTOs para requests y responses
- Estructuras de datos tipadas

### **Servicio (api/servicios/)**
- Lógica de negocio
- Interacción con el dominio
- Procesamiento de datos

### **Controlador (api/controladores/)**
- Endpoints HTTP
- Validación de entrada
- Manejo de errores
- Coordinación de servicios

## 🔒 Seguridad y Logging

- **Tokens Temporales**: Expiran automáticamente en 5 minutos
- **Validación de Clientes**: Verificación de existencia antes de operaciones
- **Logging de Transacciones**: Registro automático en `log_uvshop_transacciones_qr.log`
- **Manejo de Errores**: Respuestas HTTP apropiadas para cada caso

## 📊 Patrones de Diseño Implementados

1. **Proxy**: `ProxyPagoQR` para validación y logging
2. **Strategy**: Diferentes métodos de pago
3. **Factory**: Gestor de métodos de pago
4. **Decorator**: Beneficios adicionales para clientes
5. **Singleton**: Servicios compartidos

## 🚀 Características Avanzadas

- **Dependency Injection**: Gestión automática de dependencias
- **Documentación Automática**: Swagger UI generada automáticamente
- **Validación Robusta**: Pydantic valida todos los datos
- **Estado Compartido**: Instancias singleton mantienen datos
- **Extensibilidad**: Fácil agregar nuevos endpoints y funcionalidades

## 🎯 Comandos Útiles

### **Ejecutar servidor de desarrollo**
```bash
# Opción 1: Con recarga automática (recomendado para desarrollo)
python -m uvicorn app:app --reload --port 8000

# Opción 2: Ejecutar directamente
python app.py

# Opción 3: Con configuración específica
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### **Probar la API**
```bash
# Verificar que el servidor está funcionando
curl http://localhost:8000/

# Ver documentación
curl http://localhost:8000/docs

# Health check
curl http://localhost:8000/health/
```

### **Ejemplos del dominio (sin API)**
```bash
# Ejecutar ejemplos de las clases del dominio
python main.py
```

