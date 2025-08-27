# Sistema de Gestión de Satélites de Observación

## Descripción
Sistema distribuido para gestionar satélites de observación terrestre y espacial, permitiendo controlar la información de los satélites, sus sensores, misiones asignadas y los datos recolectados.

## Características Principales
- **Arquitectura Cliente-Servidor**: Comunicación mediante sockets TCP
- **Serialización JSON**: Intercambio de datos estructurados
- **Base de Datos**: Persistencia con SQLite
- **Concurrencia**: Soporte para múltiples clientes simultáneos
- **Modelos de Datos**: Clases estructuradas para Satélites, Misiones, Sensores y Datos

## Funcionalidades
- ✅ Registrar nuevos satélites
- ✅ Registrar y actualizar misiones de observación
- ✅ Consultar información con filtros
- ✅ Registrar y consultar datos recolectados
- ✅ Gestión de sensores a bordo

## Estructura del Proyecto
```
├── server/
│   ├── server.py          # Servidor principal
│   ├── database.py        # Gestión de base de datos
│   ├── models.py          # Modelos de datos
│   └── handlers.py        # Manejadores de requests
├── client/
│   └── client.py          # Cliente de ejemplo
├── database/
│   └── satellites.db      # Base de datos SQLite
└── README.md
```

## Instalación y Uso

### Requisitos
- Python 3.7+
- Módulos: `socket`, `json`, `sqlite3`, `threading`, `datetime`

### Ejecución
1. **Iniciar el servidor:**
   ```bash
   python server/server.py
   ```

2. **Ejecutar el cliente:**
   ```bash
   python client/client.py
   ```

## Protocolo de Comunicación
El sistema utiliza JSON para serializar las siguientes estructuras:

### Comandos del Cliente
- `REGISTER_SATELLITE`: Registrar nuevo satélite
- `REGISTER_MISSION`: Registrar nueva misión
- `QUERY_SATELLITES`: Consultar satélites
- `QUERY_MISSIONS`: Consultar misiones
- `REGISTER_DATA`: Registrar datos recolectados
- `QUERY_DATA`: Consultar datos recolectados

### Respuestas del Servidor
- `SUCCESS`: Operación exitosa
- `ERROR`: Error en la operación
- `DATA`: Datos solicitados

## Modelos de Datos

### Satélite
```json
{
  "id": "string",
  "nombre": "string",
  "tipo": "string",
  "sensores": ["array"],
  "fecha_lanzamiento": "YYYY-MM-DD",
  "orbita": "string",
  "estado": "activo|inactivo|en_mantenimiento"
}
```

### Misión
```json
{
  "id": "string",
  "satelite_id": "string",
  "objetivo": "string",
  "zona_observacion": "string",
  "duracion": "string",
  "estado": "string"
}
```

### Datos Recolectados
```json
{
  "id": "string",
  "satelite_id": "string",
  "tipo": "imagen|sensor|medicion",
  "datos": "string",
  "fecha": "YYYY-MM-DD HH:MM:SS"
}
```

