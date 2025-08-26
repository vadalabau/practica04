"""
Servidor principal del Sistema de Gestión de Satélites de Observación
Implementa comunicación TCP con serialización JSON y manejo de concurrencia
"""

import socket
import json
import threading
import sys
from typing import Dict, Any
from database import SatelliteDatabase
from handlers import RequestHandler

class SatelliteServer:
    """Servidor TCP para el Sistema de Gestión de Satélites"""
    
    def __init__(self, host: str = 'localhost', port: int = 12345):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.clients = []
        
        # Inicializar base de datos y manejador
        self.database = SatelliteDatabase()
        self.handler = RequestHandler(self.database)
        
        print("=== Sistema de Gestión de Satélites de Observación ===")
        print(f"Servidor iniciando en {host}:{port}")
        print("Base de datos inicializada")
        print("Manejador de solicitudes configurado")
        print("=" * 50)
    
    def start(self):
        """Inicia el servidor"""
        try:
            # Crear socket del servidor
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Vincular socket al puerto
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            print(f"✅ Servidor escuchando en {self.host}:{self.port}")
            print("Esperando conexiones de clientes...")
            print("Presiona Ctrl+C para detener el servidor")
            print("-" * 50)
            
            # Bucle principal para aceptar conexiones
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"Cliente conectado desde {client_address}")
                    
                    # Crear hilo para manejar el cliente
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                    self.clients.append(client_socket)
                    
                except socket.error:
                    if self.running:
                        print("❌ Error aceptando conexión")
                    break
                    
        except Exception as e:
            print(f"❌ Error iniciando servidor: {e}")
        finally:
            self.stop()
    
    def handle_client(self, client_socket: socket.socket, client_address: tuple):
        """Maneja la comunicación con un cliente específico"""
        try:
            while self.running:
                # Recibir datos del cliente
                data = client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    # Deserializar JSON del cliente
                    request_str = data.decode('utf-8')
                    print(f"Recibido de {client_address}: {request_str[:100]}...")
                    
                    request_data = json.loads(request_str)
                    
                    # Procesar solicitud
                    response = self.handler.handle_request(request_data)
                    
                    # Serializar respuesta a JSON
                    response_str = json.dumps(response, ensure_ascii=False, indent=2)
                    
                    # Enviar respuesta al cliente
                    client_socket.send(response_str.encode('utf-8'))
                    print(f"Respuesta enviada a {client_address}")
                    
                except json.JSONDecodeError as e:
                    error_response = {
                        'status': 'ERROR',
                        'message': f'Error decodificando JSON: {str(e)}'
                    }
                    client_socket.send(json.dumps(error_response).encode('utf-8'))
                    print(f"❌ Error JSON de {client_address}: {e}")
                    
                except Exception as e:
                    error_response = {
                        'status': 'ERROR',
                        'message': f'Error interno del servidor: {str(e)}'
                    }
                    client_socket.send(json.dumps(error_response).encode('utf-8'))
                    print(f"❌ Error procesando solicitud de {client_address}: {e}")
                    
        except Exception as e:
            print(f"❌ Error en comunicación con {client_address}: {e}")
        finally:
            # Limpiar conexión
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            print(f"Cliente {client_address} desconectado")
    
    def stop(self):
        """Detiene el servidor"""
        print("\nDeteniendo servidor...")
        self.running = False
        
        # Cerrar conexiones de clientes
        for client_socket in self.clients:
            try:
                client_socket.close()
            except:
                pass
        self.clients.clear()
        
        # Cerrar socket del servidor
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("✅ Servidor detenido")

def main():
    """Función principal"""
    try:
        # Configuración del servidor
        host = 'localhost'
        port = 12345
        
        # Crear e iniciar servidor
        server = SatelliteServer(host, port)
        server.start()
        
    except KeyboardInterrupt:
        print("\nInterrupción del usuario detectada")
    except Exception as e:
        print(f"❌ Error fatal: {e}")
    finally:
        print("¡Hasta luego!")

if __name__ == "__main__":
    main()
