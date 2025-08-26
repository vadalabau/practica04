"""
Cliente demo para el Sistema de Gestión de Satélites
Demuestra múltiples clientes conectándose simultáneamente
"""

import socket
import json
import threading
import time

def cliente_worker(cliente_id):
    """Función que ejecuta un cliente individual"""
    print(f"Cliente {cliente_id} iniciando...")
    
    try:
        # Conectar al servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 12345))
            print(f"Cliente {cliente_id} conectado")
            
            # Registrar satélite
            solicitud = {
                "action": "register_satellite",
                "data": {
                    "nombre": f"Satélite-{cliente_id}",
                    "tipo": "Observación",
                    "fecha_lanzamiento": "2024-01-15",
                    "orbita": "LEO",
                    "sensores": [{"nombre": "Cámara", "tipo": "Óptico"}]
                }
            }
            
            s.send(json.dumps(solicitud).encode('utf-8'))
            respuesta = json.loads(s.recv(4096).decode('utf-8'))
            print(f"✅ Cliente {cliente_id}: Satélite registrado")
            
            # Consultar satélites
            solicitud = {"action": "query_satellites"}
            s.send(json.dumps(solicitud).encode('utf-8'))
            respuesta = json.loads(s.recv(4096).decode('utf-8'))
            satelites = respuesta.get('data', {}).get('satelites', [])
            print(f"✅ Cliente {cliente_id}: Encontrados {len(satelites)} satélites")
            
            print(f"🔌 Cliente {cliente_id} desconectado")
            
    except Exception as e:
        print(f"❌ Cliente {cliente_id} error: {e}")

def main():
    """Función principal"""
    print("=== Demo: Múltiples Clientes Simultáneos ===")
    
    # Verificar que el servidor esté funcionando
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect(('localhost', 12345))
            print("✅ Servidor está funcionando")
    except:
        print("❌ Servidor no está disponible")
        print("Ejecuta 'python server/server.py' primero")
        return
    
    print("\nIniciando 3 clientes simultáneamente...")
    
    # Crear hilos para múltiples clientes
    hilos = []
    for i in range(3):
        hilo = threading.Thread(target=cliente_worker, args=(i+1,))
        hilo.daemon = True
        hilos.append(hilo)
    
    # Iniciar todos los hilos
    for hilo in hilos:
        hilo.start()
        time.sleep(0.1)
    
    # Esperar a que terminen todos los hilos
    for hilo in hilos:
        hilo.join()
    
    print("\nDemo completado!")

if __name__ == "__main__":
    main()
