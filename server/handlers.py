"""
Manejadores de solicitudes para el Sistema de Gestión de Satélites
Procesa comandos del cliente usando serialización JSON
"""

import json
from typing import Dict, Any, List
from models import Satelite, Mision, DatosRecolectados, Sensor, serialize_to_json, deserialize_from_json
from database import SatelliteDatabase

class RequestHandler:
    """Manejador principal de solicitudes del cliente"""
    
    def __init__(self, database: SatelliteDatabase):
        self.db = database
    
    def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja una solicitud del cliente y retorna la respuesta"""
        try:
            # Soporte tanto 'command' como 'action' para compatibilidad
            command = request_data.get('command') or request_data.get('action')
            
            if command == 'REGISTER_SATELLITE' or command == 'register_satellite':
                return self.handle_register_satellite(request_data)
            elif command == 'REGISTER_MISSION' or command == 'register_mission':
                return self.handle_register_mission(request_data)
            elif command == 'QUERY_SATELLITES' or command == 'query_satellites':
                return self.handle_query_satellites(request_data)
            elif command == 'QUERY_MISSIONS' or command == 'query_missions':
                return self.handle_query_missions(request_data)
            elif command == 'REGISTER_DATA' or command == 'register_data':
                return self.handle_register_data(request_data)
            elif command == 'QUERY_DATA' or command == 'query_data':
                return self.handle_query_data(request_data)
            elif command == 'GET_STATISTICS' or command == 'get_statistics':
                return self.handle_get_statistics(request_data)
            else:
                return {
                    'status': 'ERROR',
                    'message': f'Comando no reconocido: {command}'
                }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Error procesando solicitud: {str(e)}'
            }
    
    def handle_register_satellite(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja el registro de un nuevo satélite"""
        try:
            satellite_data = request_data.get('data', {})
            
            # Crear sensores desde los datos
            sensores = []
            for sensor_data in satellite_data.get('sensores', []):
                sensor = Sensor(
                    nombre=sensor_data['nombre'],
                    tipo=sensor_data['tipo'],
                    descripcion=sensor_data.get('descripcion', '')
                )
                sensores.append(sensor)
            
            # Crear el satélite
            satelite = Satelite(
                nombre=satellite_data['nombre'],
                tipo=satellite_data['tipo'],
                fecha_lanzamiento=satellite_data['fecha_lanzamiento'],
                orbita=satellite_data['orbita'],
                estado=satellite_data.get('estado', 'activo'),
                sensores=sensores
            )
            
            # Guardar en la base de datos
            if self.db.guardar_satelite(satelite):
                return {
                    'status': 'SUCCESS',
                    'message': 'Satélite registrado exitosamente',
                    'data': {
                        'id': satelite.id,
                        'satelite': satelite.to_dict()
                    }
                }
            else:
                return {
                    'status': 'ERROR',
                    'message': 'Error al guardar el satélite en la base de datos'
                }
        except KeyError as e:
            return {
                'status': 'ERROR',
                'message': f'Datos faltantes: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Error registrando satélite: {str(e)}'
            }
    
    def handle_register_mission(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja el registro de una nueva misión"""
        try:
            mission_data = request_data.get('data', {})
            
            # Verificar que el satélite existe
            satelite = self.db.obtener_satelite(mission_data['satelite_id'])
            if not satelite:
                return {
                    'status': 'ERROR',
                    'message': 'El satélite especificado no existe'
                }
            
            # Crear la misión
            mision = Mision(
                satelite_id=mission_data['satelite_id'],
                objetivo=mission_data['objetivo'],
                zona_observacion=mission_data['zona_observacion'],
                duracion=mission_data['duracion'],
                estado=mission_data.get('estado', 'planificada')
            )
            
            # Guardar en la base de datos
            if self.db.guardar_mision(mision):
                return {
                    'status': 'SUCCESS',
                    'message': 'Misión registrada exitosamente',
                    'data': {
                        'id': mision.id,
                        'mision': mision.to_dict()
                    }
                }
            else:
                return {
                    'status': 'ERROR',
                    'message': 'Error al guardar la misión en la base de datos'
                }
        except KeyError as e:
            return {
                'status': 'ERROR',
                'message': f'Datos faltantes: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Error registrando misión: {str(e)}'
            }
    
    def handle_query_satellites(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja la consulta de satélites"""
        try:
            filtros = request_data.get('filtros', {})
            
            # Aplicar filtros
            satelites = self.db.listar_satelites(filtros)
            
            # Serializar a JSON
            satelites_data = [satelite.to_dict() for satelite in satelites]
            
            return {
                'status': 'SUCCESS',
                'message': f'Se encontraron {len(satelites)} satélites',
                'data': {
                    'satelites': satelites_data,
                    'total': len(satelites)
                }
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Error consultando satélites: {str(e)}'
            }
    
    def handle_query_missions(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja la consulta de misiones"""
        try:
            filtros = request_data.get('filtros', {})
            
            # Aplicar filtros
            misiones = self.db.listar_misiones(filtros)
            
            # Serializar a JSON
            misiones_data = [mision.to_dict() for mision in misiones]
            
            return {
                'status': 'SUCCESS',
                'message': f'Se encontraron {len(misiones)} misiones',
                'data': {
                    'misiones': misiones_data,
                    'total': len(misiones)
                }
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Error consultando misiones: {str(e)}'
            }
    
    def handle_register_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja el registro de datos recolectados"""
        try:
            data_info = request_data.get('data', {})
            
            # Verificar que el satélite existe
            satelite = self.db.obtener_satelite(data_info['satelite_id'])
            if not satelite:
                return {
                    'status': 'ERROR',
                    'message': 'El satélite especificado no existe'
                }
            
            # Crear los datos recolectados
            datos = DatosRecolectados(
                satelite_id=data_info['satelite_id'],
                tipo=data_info['tipo'],
                datos=data_info['datos']
            )
            
            # Guardar en la base de datos
            if self.db.guardar_datos_recolectados(datos):
                return {
                    'status': 'SUCCESS',
                    'message': 'Datos recolectados registrados exitosamente',
                    'data': {
                        'id': datos.id,
                        'datos': datos.to_dict()
                    }
                }
            else:
                return {
                    'status': 'ERROR',
                    'message': 'Error al guardar los datos en la base de datos'
                }
        except KeyError as e:
            return {
                'status': 'ERROR',
                'message': f'Datos faltantes: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Error registrando datos: {str(e)}'
            }
    
    def handle_query_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja la consulta de datos recolectados"""
        try:
            filtros = request_data.get('filtros', {})
            
            # Aplicar filtros
            datos_list = self.db.listar_datos_recolectados(filtros)
            
            # Serializar a JSON
            datos_data = [datos.to_dict() for datos in datos_list]
            
            return {
                'status': 'SUCCESS',
                'message': f'Se encontraron {len(datos_list)} registros de datos',
                'data': {
                    'datos': datos_data,
                    'total': len(datos_list)
                }
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Error consultando datos: {str(e)}'
            }
    
    def handle_get_statistics(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Maneja la obtención de estadísticas del sistema"""
        try:
            estadisticas = self.db.obtener_estadisticas()
            
            return {
                'status': 'SUCCESS',
                'message': 'Estadísticas obtenidas exitosamente',
                'data': estadisticas
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'message': f'Error obteniendo estadísticas: {str(e)}'
            }
