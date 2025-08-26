"""
Cliente de ejemplo para el Sistema de Gestión de Satélites de Observación
Demuestra el uso de serialización JSON y comunicación TCP
"""

import socket
import json
import time
from typing import Dict, Any

class SatelliteClient:
    """Cliente para comunicarse con el servidor de satélites"""
    
    def __init__(self, host: str = 'localhost', port: int = 12345):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self) -> bool:
        """Conecta al servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"✅ Conectado al servidor en {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ Error conectando al servidor: {e}")
            return False
    
    def disconnect(self):
        """Desconecta del servidor"""
        if self.socket:
            self.socket.close()
            print("Desconectado del servidor")
    
    def send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Envía una solicitud al servidor y recibe la respuesta"""
        try:
            # Serializar solicitud a JSON
            request_str = json.dumps(request, ensure_ascii=False, indent=2)
            print(f"Enviando: {request_str}")
            
            # Enviar al servidor
            self.socket.send(request_str.encode('utf-8'))
            
            # Recibir respuesta
            response_data = self.socket.recv(4096)
            response_str = response_data.decode('utf-8')
            
            # Deserializar respuesta JSON
            response = json.loads(response_str)
            print(f"Respuesta: {json.dumps(response, ensure_ascii=False, indent=2)}")
            
            return response
            
        except Exception as e:
            print(f"❌ Error en comunicación: {e}")
            return {'status': 'ERROR', 'message': str(e)}

def demo_satellite_system():
    """Demuestra todas las funcionalidades del sistema"""
    print("=== DEMO: Sistema de Gestión de Satélites de Observación ===")
    print("Este demo muestra la serialización JSON y comunicación TCP")
    print("=" * 60)
    
    # Crear cliente
    client = SatelliteClient()
    
    if not client.connect():
        print("❌ No se pudo conectar al servidor. Asegúrate de que esté ejecutándose.")
        return
    
    try:
        # 1. REGISTRAR SATÉLITES
        print("\n1. REGISTRANDO SATÉLITES")
        print("-" * 40)
        
        # Satélite 1: Observación terrestre
        satelite1_data = {
            "command": "REGISTER_SATELLITE",
            "data": {
                "nombre": "Satélite Observación Terrestre 1",
                "tipo": "observacion_terrestre",
                "fecha_lanzamiento": "2023-01-15",
                "orbita": "Órbita baja terrestre (LEO)",
                "estado": "activo",
                "sensores": [
                    {
                        "nombre": "Cámara Multiespectral",
                        "tipo": "óptico",
                        "descripcion": "Captura imágenes en múltiples bandas espectrales"
                    },
                    {
                        "nombre": "Radar de Apertura Sintética",
                        "tipo": "radar",
                        "descripcion": "Imágenes radar independientes del clima"
                    },
                    {
                        "nombre": "Sensor Infrarrojo",
                        "tipo": "infrarrojo",
                        "descripcion": "Detección de calor y temperatura"
                    }
                ]
            }
        }
        
        response1 = client.send_request(satelite1_data)
        satelite1_id = response1.get('data', {}).get('id') if response1['status'] == 'SUCCESS' else None
        
        # Satélite 2: Meteorológico
        satelite2_data = {
            "command": "REGISTER_SATELLITE",
            "data": {
                "nombre": "Satélite Meteorológico Global",
                "tipo": "meteorologico",
                "fecha_lanzamiento": "2023-03-20",
                "orbita": "Órbita geoestacionaria",
                "estado": "activo",
                "sensores": [
                    {
                        "nombre": "Radiómetro Infrarrojo",
                        "tipo": "infrarrojo",
                        "descripcion": "Medición de temperatura atmosférica"
                    },
                    {
                        "nombre": "Sensor de Vapor de Agua",
                        "tipo": "microondas",
                        "descripcion": "Humedad atmosférica"
                    }
                ]
            }
        }
        
        response2 = client.send_request(satelite2_data)
        satelite2_id = response2.get('data', {}).get('id') if response2['status'] == 'SUCCESS' else None
        
        time.sleep(1)
        
        # 2. REGISTRAR MISIONES
        print("\n2. REGISTRANDO MISIONES")
        print("-" * 40)
        
        if satelite1_id:
            mision1_data = {
                "command": "REGISTER_MISSION",
                "data": {
                    "satelite_id": satelite1_id,
                    "objetivo": "Monitoreo de deforestación en Amazonas",
                    "zona_observacion": "Región amazónica, Brasil",
                    "duracion": "6 meses",
                    "estado": "en_ejecucion"
                }
            }
            client.send_request(mision1_data)
        
        if satelite2_id:
            mision2_data = {
                "command": "REGISTER_MISSION",
                "data": {
                    "satelite_id": satelite2_id,
                    "objetivo": "Predicción meteorológica global",
                    "zona_observacion": "Hemisferio occidental",
                    "duracion": "12 meses",
                    "estado": "en_ejecucion"
                }
            }
            client.send_request(mision2_data)
        
        time.sleep(1)
        
        # 3. REGISTRAR DATOS RECOLECTADOS
        print("\n3. REGISTRANDO DATOS RECOLECTADOS")
        print("-" * 40)
        
        if satelite1_id:
            # Datos de imagen
            datos1 = {
                "command": "REGISTER_DATA",
                "data": {
                    "satelite_id": satelite1_id,
                    "tipo": "imagen",
                    "datos": "Imagen multiespectral de alta resolución - Coordenadas: -3.4653, -58.3804 - Fecha: 2024-01-15 10:30:00"
                }
            }
            client.send_request(datos1)
            
            # Datos de sensor
            datos2 = {
                "command": "REGISTER_DATA",
                "data": {
                    "satelite_id": satelite1_id,
                    "tipo": "sensor",
                    "datos": "Lectura radar SAR - Cobertura nubosa: 15% - Visibilidad: excelente - Resolución: 10m"
                }
            }
            client.send_request(datos2)
        
        if satelite2_id:
            # Datos meteorológicos
            datos3 = {
                "command": "REGISTER_DATA",
                "data": {
                    "satelite_id": satelite2_id,
                    "tipo": "medicion",
                    "datos": "Temperatura atmosférica: 22.5°C - Humedad: 65% - Presión: 1013.25 hPa - Viento: 15 km/h NE"
                }
            }
            client.send_request(datos3)
        
        time.sleep(1)
        
        # 4. CONSULTAR SATÉLITES
        print("\n4. CONSULTANDO SATÉLITES")
        print("-" * 40)
        
        # Todos los satélites
        consulta_satelites = {
            "command": "QUERY_SATELLITES",
            "filtros": {}
        }
        client.send_request(consulta_satelites)
        
        # Satélites activos
        consulta_activos = {
            "command": "QUERY_SATELLITES",
            "filtros": {"estado": "activo"}
        }
        client.send_request(consulta_activos)
        
        # Satélites de observación terrestre
        consulta_observacion = {
            "command": "QUERY_SATELLITES",
            "filtros": {"tipo": "observacion_terrestre"}
        }
        client.send_request(consulta_observacion)
        
        time.sleep(1)
        
        # 5. CONSULTAR MISIONES
        print("\n5. CONSULTANDO MISIONES")
        print("-" * 40)
        
        # Todas las misiones
        consulta_misiones = {
            "command": "QUERY_MISSIONS",
            "filtros": {}
        }
        client.send_request(consulta_misiones)
        
        # Misiones en ejecución
        consulta_ejecucion = {
            "command": "QUERY_MISSIONS",
            "filtros": {"estado": "en_ejecucion"}
        }
        client.send_request(consulta_ejecucion)
        
        time.sleep(1)
        
        # 6. CONSULTAR DATOS RECOLECTADOS
        print("\n6. CONSULTANDO DATOS RECOLECTADOS")
        print("-" * 40)
        
        # Todos los datos
        consulta_datos = {
            "command": "QUERY_DATA",
            "filtros": {}
        }
        client.send_request(consulta_datos)
        
        # Datos de imágenes
        consulta_imagenes = {
            "command": "QUERY_DATA",
            "filtros": {"tipo": "imagen"}
        }
        client.send_request(consulta_imagenes)
        
        time.sleep(1)
        
        # 7. OBTENER ESTADÍSTICAS
        print("\n7. ESTADÍSTICAS DEL SISTEMA")
        print("-" * 40)
        
        estadisticas = {
            "command": "GET_STATISTICS"
        }
        client.send_request(estadisticas)
        
        print("\n" + "=" * 60)
        print("✅ DEMO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print("\nEste demo demostró:")
        print("   • Serialización y deserialización JSON")
        print("   • Comunicación TCP cliente-servidor")
        print("   • Manejo de estructuras de datos complejas")
        print("   • Persistencia en base de datos")
        print("   • Consultas con filtros")
        print("   • Gestión de satélites, misiones y datos")
        
    except Exception as e:
        print(f"❌ Error durante el demo: {e}")
    finally:
        client.disconnect()

def interactive_mode():
    """Modo interactivo para probar comandos manualmente"""
    print("\nMODO INTERACTIVO")
    print("Escribe comandos JSON o 'quit' para salir")
    print("-" * 40)
    
    client = SatelliteClient()
    if not client.connect():
        return
    
    try:
        while True:
            try:
                user_input = input("\nIngresa comando JSON: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'salir']:
                    break
                
                if not user_input:
                    continue
                
                # Intentar parsear como JSON
                request = json.loads(user_input)
                response = client.send_request(request)
                
            except json.JSONDecodeError:
                print("❌ Error: Formato JSON inválido")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    finally:
        client.disconnect()

def main():
    """Función principal"""
    print("🛰️  Cliente del Sistema de Gestión de Satélites")
    print("=" * 50)
    
    while True:
        print("\nOpciones:")
        print("1. Ejecutar demo completo")
        print("2. Modo interactivo")
        print("3. Salir")
        
        choice = input("\nSelecciona una opción (1-3): ").strip()
        
        if choice == '1':
            demo_satellite_system()
        elif choice == '2':
            interactive_mode()
        elif choice == '3':
            print("¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()
