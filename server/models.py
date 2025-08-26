"""
Modelos de datos para el Sistema de Gestión de Satélites de Observación
Implementa serialización y deserialización JSON para comunicación distribuida
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

class Sensor:
    """Modelo para representar sensores a bordo de satélites"""
    
    def __init__(self, nombre: str, tipo: str, descripcion: str = ""):
        self.nombre = nombre
        self.tipo = tipo
        self.descripcion = descripcion
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el sensor a diccionario para JSON"""
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "descripcion": self.descripcion
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Sensor':
        """Deserializa diccionario a objeto Sensor"""
        return Sensor(
            nombre=data["nombre"],
            tipo=data["tipo"],
            descripcion=data.get("descripcion", "")
        )
    
    def __str__(self) -> str:
        return f"Sensor({self.nombre}, {self.tipo})"

class Satelite:
    """Modelo para representar satélites de observación"""
    
    def __init__(self, nombre: str, tipo: str, fecha_lanzamiento: str, 
                 orbita: str, estado: str = "activo", sensores: List[Sensor] = None):
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.tipo = tipo
        self.fecha_lanzamiento = fecha_lanzamiento
        self.orbita = orbita
        self.estado = estado
        self.sensores = sensores or []
    
    def agregar_sensor(self, sensor: Sensor):
        """Agrega un sensor al satélite"""
        self.sensores.append(sensor)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa el satélite a diccionario para JSON"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "fecha_lanzamiento": self.fecha_lanzamiento,
            "orbita": self.orbita,
            "estado": self.estado,
            "sensores": [sensor.to_dict() for sensor in self.sensores]
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Satelite':
        """Deserializa diccionario a objeto Satelite"""
        satelite = Satelite(
            nombre=data["nombre"],
            tipo=data["tipo"],
            fecha_lanzamiento=data["fecha_lanzamiento"],
            orbita=data["orbita"],
            estado=data.get("estado", "activo")
        )
        satelite.id = data.get("id", str(uuid.uuid4()))
        
        # Deserializar sensores
        if "sensores" in data:
            satelite.sensores = [Sensor.from_dict(sensor_data) for sensor_data in data["sensores"]]
        
        return satelite
    
    def __str__(self) -> str:
        return f"Satélite({self.nombre}, {self.tipo}, {self.estado})"

class Mision:
    """Modelo para representar misiones de observación"""
    
    def __init__(self, satelite_id: str, objetivo: str, zona_observacion: str, 
                 duracion: str, estado: str = "planificada"):
        self.id = str(uuid.uuid4())
        self.satelite_id = satelite_id
        self.objetivo = objetivo
        self.zona_observacion = zona_observacion
        self.duracion = duracion
        self.estado = estado
        self.fecha_creacion = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa la misión a diccionario para JSON"""
        return {
            "id": self.id,
            "satelite_id": self.satelite_id,
            "objetivo": self.objetivo,
            "zona_observacion": self.zona_observacion,
            "duracion": self.duracion,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Mision':
        """Deserializa diccionario a objeto Mision"""
        mision = Mision(
            satelite_id=data["satelite_id"],
            objetivo=data["objetivo"],
            zona_observacion=data["zona_observacion"],
            duracion=data["duracion"],
            estado=data.get("estado", "planificada")
        )
        mision.id = data.get("id", str(uuid.uuid4()))
        mision.fecha_creacion = data.get("fecha_creacion", datetime.now().isoformat())
        return mision
    
    def __str__(self) -> str:
        return f"Misión({self.objetivo}, {self.estado})"

class DatosRecolectados:
    """Modelo para representar datos recolectados por los satélites"""
    
    def __init__(self, satelite_id: str, tipo: str, datos: str):
        self.id = str(uuid.uuid4())
        self.satelite_id = satelite_id
        self.tipo = tipo  # "imagen", "sensor", "medicion"
        self.datos = datos
        self.fecha = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa los datos recolectados a diccionario para JSON"""
        return {
            "id": self.id,
            "satelite_id": self.satelite_id,
            "tipo": self.tipo,
            "datos": self.datos,
            "fecha": self.fecha
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'DatosRecolectados':
        """Deserializa diccionario a objeto DatosRecolectados"""
        datos_recolectados = DatosRecolectados(
            satelite_id=data["satelite_id"],
            tipo=data["tipo"],
            datos=data["datos"]
        )
        datos_recolectados.id = data.get("id", str(uuid.uuid4()))
        datos_recolectados.fecha = data.get("fecha", datetime.now().isoformat())
        return datos_recolectados
    
    def __str__(self) -> str:
        return f"Datos({self.tipo}, {self.satelite_id}, {self.fecha})"

# Funciones de utilidad para serialización JSON
def serialize_to_json(obj) -> str:
    """Serializa un objeto a string JSON"""
    if hasattr(obj, 'to_dict'):
        return json.dumps(obj.to_dict(), ensure_ascii=False, indent=2)
    elif isinstance(obj, list):
        return json.dumps([item.to_dict() if hasattr(item, 'to_dict') else item for item in obj], 
                         ensure_ascii=False, indent=2)
    else:
        return json.dumps(obj, ensure_ascii=False, indent=2)

def deserialize_from_json(json_str: str, model_class=None):
    """Deserializa string JSON a objeto"""
    data = json.loads(json_str)
    
    if model_class and hasattr(model_class, 'from_dict'):
        if isinstance(data, list):
            return [model_class.from_dict(item) for item in data]
        else:
            return model_class.from_dict(data)
    
    return data
