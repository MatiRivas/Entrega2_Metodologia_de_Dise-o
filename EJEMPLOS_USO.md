# Ejemplos de Uso - UVShop API MVC

## Introducción
Este documento muestra ejemplos prácticos de cómo usar la API de UVShop con la nueva estructura MVC.

## Configuración Base

### 1. Ejecutar el servidor
```bash
python -m uvicorn app:app --reload --port 8000
```

### 2. Acceder a la documentación interactiva
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Ejemplos de Peticiones

### 1. Crear Cliente
```bash
curl -X POST "http://localhost:8000/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@email.com",
    "direccion": "Calle 123",
    "tipo_cliente": "VIP"
  }'
```

**Respuesta:**
```json
{
  "message": "Cliente creado exitosamente",
  "cliente": {
    "email": "juan@email.com",
    "nombre": "Juan Pérez",
    "tipo": "VIP",
    "descuento": 0.15,
    "direccion": "Calle 123"
  }
}
```

### 2. Crear Producto
```bash
curl -X POST "http://localhost:8000/productos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Gaming",
    "codigo": "LAP001",
    "precio": 1500.00,
    "stock": 10
  }'
```

**Respuesta:**
```json
{
  "message": "Producto creado exitosamente",
  "producto": {
    "codigo": "LAP001",
    "nombre": "Laptop Gaming",
    "precio": 1500.0,
    "stock": 10
  }
}
```

### 3. Generar Token para Pago QR
```bash
curl -X POST "http://localhost:8000/tokens/generar" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_email": "juan@email.com"
  }'
```

**Respuesta:**
```json
{
  "token": "abc123token456",
  "expires_in_seconds": 300,
  "cliente_email": "juan@email.com"
}
```

### 4. Procesar Pago QR
```bash
curl -X POST "http://localhost:8000/pagos/procesar" \
  -H "Content-Type: application/json" \
  -d '{
    "pedido_id": 1,
    "metodo_pago": "qr",
    "monto": 1275.00,
    "cliente_email": "juan@email.com",
    "token_temporal": "abc123token456"
  }'
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Pago procesado exitosamente",
  "metodo_pago": "qr",
  "monto": 1275.0,
  "cliente_email": "juan@email.com",
  "transaction_id": null
}
```

### 5. Procesar Pago con Tarjeta
```bash
curl -X POST "http://localhost:8000/pagos/procesar" \
  -H "Content-Type: application/json" \
  -d '{
    "pedido_id": 2,
    "metodo_pago": "tarjeta",
    "monto": 1500.00,
    "cliente_email": "juan@email.com"
  }'
```

### 6. Listar Clientes
```bash
curl -X GET "http://localhost:8000/clientes/"
```

### 7. Listar Productos
```bash
curl -X GET "http://localhost:8000/productos/"
```

### 8. Obtener Métodos de Pago
```bash
curl -X GET "http://localhost:8000/pagos/metodos"
```

**Respuesta:**
```json
{
  "metodos_pago": ["tarjeta", "qr"]
}
```

### 9. Health Check
```bash
curl -X GET "http://localhost:8000/health/"
```

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "UVShop API"
}
```

## Flujo Completo de Compra

### Paso 1: Crear Cliente y Producto
```bash
# Cliente
curl -X POST "http://localhost:8000/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María García",
    "email": "maria@email.com",
    "direccion": "Avenida Principal 456",
    "tipo_cliente": "FRECUENTE"
  }'

# Producto
curl -X POST "http://localhost:8000/productos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Mouse Inalámbrico",
    "codigo": "MOU001",
    "precio": 25.99,
    "stock": 50
  }'
```

### Paso 2: Generar Token QR
```bash
curl -X POST "http://localhost:8000/tokens/generar" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_email": "maria@email.com"
  }'
```

### Paso 3: Procesar Pago QR
```bash
curl -X POST "http://localhost:8000/pagos/procesar" \
  -H "Content-Type: application/json" \
  -d '{
    "pedido_id": 3,
    "metodo_pago": "qr",
    "monto": 22.09,
    "cliente_email": "maria@email.com",
    "token_temporal": "[TOKEN_OBTENIDO]"
  }'
```

## Manejo de Errores

### Cliente No Encontrado
```bash
curl -X POST "http://localhost:8000/pagos/procesar" \
  -H "Content-Type: application/json" \
  -d '{
    "pedido_id": 1,
    "metodo_pago": "qr",
    "monto": 100.00,
    "cliente_email": "noexiste@email.com",
    "token_temporal": "token123"
  }'
```

**Respuesta de Error:**
```json
{
  "detail": "Cliente no encontrado"
}
```

### Token Faltante para QR
```bash
curl -X POST "http://localhost:8000/pagos/procesar" \
  -H "Content-Type: application/json" \
  -d '{
    "pedido_id": 1,
    "metodo_pago": "qr",
    "monto": 100.00,
    "cliente_email": "juan@email.com"
  }'
```

**Respuesta de Error:**
```json
{
  "detail": "Token temporal requerido para pago QR"
}
```

## Validación de Datos

### Tipo de Cliente Inválido
```bash
curl -X POST "http://localhost:8000/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Cliente Test",
    "email": "test@email.com",
    "direccion": "Dirección Test",
    "tipo_cliente": "INVALIDO"
  }'
```

### Email Inválido
```bash
curl -X POST "http://localhost:8000/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Cliente Test",
    "email": "email-invalido",
    "direccion": "Dirección Test",
    "tipo_cliente": "NORMAL"
  }'
```

## Características de la Nueva Estructura

### 1. **Separación de Responsabilidades**
- **Controladores**: Manejan HTTP y validación
- **Servicios**: Lógica de negocio
- **Modelos**: Estructuras de datos

### 2. **Manejo de Estados**
- Instancias singleton mantienen datos entre requests
- Estado compartido entre diferentes endpoints

### 3. **Validación Robusta**
- Pydantic valida automáticamente los datos
- Errores claros y específicos

### 4. **Extensibilidad**
- Fácil agregar nuevos endpoints
- Servicios reutilizables

## Logs y Auditoria

Los pagos QR son registrados automáticamente en el archivo `log_uvshop_transacciones_qr.log` gracias al patrón Proxy implementado.

## Conclusión

La nueva estructura MVC proporciona:
- ✅ Código más organizado y mantenible
- ✅ Separación clara de responsabilidades
- ✅ Fácil testing y debugging
- ✅ Escalabilidad para futuras funcionalidades
- ✅ Documentación automática con FastAPI
