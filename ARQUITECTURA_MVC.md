# Estructura MVC - UVShop API

## Descripción General
Se ha implementado una arquitectura MVC (Model-View-Controller) para organizar la API de UVShop de manera escalable y mantenible.

## Estructura de Carpetas

```
api/
├── __init__.py
├── dependencies.py                 # Gestión de dependencias singleton
├── modelos/
│   ├── __init__.py
│   └── schemas.py                 # DTOs/Schemas de Pydantic
├── servicios/
│   ├── __init__.py
│   ├── cliente_service.py         # Lógica de negocio - Clientes
│   ├── producto_service.py        # Lógica de negocio - Productos
│   ├── token_service.py           # Lógica de negocio - Tokens
│   └── pago_service.py            # Lógica de negocio - Pagos
└── controladores/
    ├── __init__.py
    ├── main_router.py             # Router principal
    ├── cliente_controller.py      # Endpoints - Clientes
    ├── producto_controller.py     # Endpoints - Productos
    ├── token_controller.py        # Endpoints - Tokens
    ├── pago_controller.py         # Endpoints - Pagos
    └── health_controller.py       # Endpoints - Health check
```

## Componentes de la Arquitectura

### 1. **Modelos (api/modelos/)**
- **Propósito**: Definir la estructura de datos de entrada y salida
- **Responsabilidades**:
  - Schemas de Pydantic para validación
  - DTOs (Data Transfer Objects) para requests y responses
  - Modelos de validación de datos

### 2. **Servicios (api/servicios/)**
- **Propósito**: Contener la lógica de negocio
- **Responsabilidades**:
  - Interactuar con el dominio de la aplicación (src/)
  - Procesar datos de negocio
  - Manejar transacciones y operaciones complejas
  - Validaciones de negocio

### 3. **Controladores (api/controladores/)**
- **Propósito**: Manejar las requests HTTP y coordinar respuestas
- **Responsabilidades**:
  - Definir endpoints y rutas
  - Validar datos de entrada
  - Coordinar servicios
  - Manejar errores HTTP
  - Formatear respuestas

### 4. **Dependencias (api/dependencies.py)**
- **Propósito**: Gestionar instancias singleton de servicios
- **Responsabilidades**:
  - Crear instancias únicas de servicios
  - Mantener estado compartido entre requests
  - Facilitar dependency injection

## Endpoints Disponibles

### Clientes
- `POST /clientes/` - Crear cliente
- `GET /clientes/` - Listar clientes
- `GET /clientes/{email}` - Obtener cliente específico

### Productos
- `POST /productos/` - Crear producto
- `GET /productos/` - Listar productos
- `GET /productos/{codigo}` - Obtener producto específico

### Tokens
- `POST /tokens/generar` - Generar token temporal
- `POST /tokens/validar` - Validar token temporal

### Pagos
- `POST /pagos/procesar` - Procesar pago
- `GET /pagos/metodos` - Obtener métodos de pago disponibles

### Health Check
- `GET /health/` - Estado del sistema
- `GET /health/info` - Información del sistema

### General
- `GET /` - Mensaje de bienvenida

## Flujo de Datos

```
Request → Controlador → Servicio → Dominio (src/) → Respuesta
```

1. **Request**: El cliente envía una petición HTTP
2. **Controlador**: Valida la entrada y delega al servicio correspondiente
3. **Servicio**: Procesa la lógica de negocio usando el dominio
4. **Dominio**: Ejecuta las operaciones core del sistema
5. **Respuesta**: Se devuelve la respuesta formateada al cliente

## Beneficios de la Arquitectura MVC

1. **Separación de Responsabilidades**: Cada capa tiene una responsabilidad específica
2. **Mantenibilidad**: Fácil de mantener y actualizar
3. **Escalabilidad**: Fácil agregar nuevas funcionalidades
4. **Testabilidad**: Cada capa puede ser probada independientemente
5. **Reutilización**: Los servicios pueden ser reutilizados por múltiples controladores

## Gestión de Estados

- **Singleton Pattern**: Los servicios mantienen instancias únicas
- **Estado Compartido**: Los datos se comparten entre requests
- **Dependency Injection**: FastAPI gestiona las dependencias automáticamente

## Cómo Ejecutar

```bash
# Instalar dependencias
pip install fastapi uvicorn pydantic

# Ejecutar servidor
python -m uvicorn app:app --reload --port 8000

# Acceder a la documentación
http://localhost:8000/docs
```

## Próximos Pasos

1. Implementar base de datos real (SQLAlchemy)
2. Agregar autenticación JWT
3. Implementar tests unitarios
4. Agregar logging centralizado
5. Implementar cache (Redis)
6. Agregar monitoreo y métricas
