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
            
            satelite_nombre = f"Satélite-{cliente_id}-{time.time_ns()}"

            # 1. Registrar satélite
            solicitud_satelite = {
                "accion": "registrar_satelite", # Usar "registrar_satelite" para compatibilidad con server.py
                "nombre": satelite_nombre,
                "tipo": "Observación",
                "fecha_lanzamiento": "2024-01-15",
                "orbita": "LEO",
                "estado": "activo",
                "sensores": json.dumps([{"nombre": "Cámara", "tipo": "Óptico"}]) # Los sensores deben ser un string JSON
            }
            
            s.send(json.dumps(solicitud_satelite).encode('utf-8'))
            respuesta_satelite = json.loads(s.recv(4096).decode('utf-8'))
            print(f"✅ Cliente {cliente_id}: Registro Satélite: {respuesta_satelite}")

            # 2. Consultar satélites
            solicitud_consulta_satelites = {"accion": "consultar_satelites"}
            s.send(json.dumps(solicitud_consulta_satelites).encode('utf-8'))
            respuesta_consulta_satelites = json.loads(s.recv(4096).decode('utf-8'))
            
            satelites_encontrados = respuesta_consulta_satelites.get('data', {}).get('satelites', [])
            print(f"✅ Cliente {cliente_id}: Encontrados {len(satelites_encontrados)} satélites después de registro")
            
            # 3. Registrar misión (usando el satélite recién registrado)
            if respuesta_satelite.get("status") == "success":
                solicitud_mision = {
                    "accion": "registrar_mision",
                    "satelite_nombre": satelite_nombre,
                    "objetivo": f"Misión de {satelite_nombre}",
                    "zona": "Andes",
                    "duracion": 30,
                    "estado": "planificada"
                }
                s.send(json.dumps(solicitud_mision).encode('utf-8'))
                respuesta_mision = json.loads(s.recv(4096).decode('utf-8'))
                print(f"✅ Cliente {cliente_id}: Registro Misión: {respuesta_mision}")

            # 4. Consultar misiones
            solicitud_consulta_misiones = {"accion": "consultar_misiones"}
            s.send(json.dumps(solicitud_consulta_misiones).encode('utf-8'))
            respuesta_consulta_misiones = json.loads(s.recv(4096).decode('utf-8'))
            
            misiones_encontradas = respuesta_consulta_misiones.get('data', {}).get('misiones', [])
            print(f"✅ Cliente {cliente_id}: Encontradas {len(misiones_encontradas)} misiones")

            # 5. Registrar dato
            if respuesta_satelite.get("status") == "success":
                solicitud_dato = {
                    "accion": "registrar_dato",
                    "satelite_nombre": satelite_nombre,
                    "tipo": "imagen",
                    "valor": "base64_imagen_simulada",
                    "fecha": "2024-01-15"
                }
                s.send(json.dumps(solicitud_dato).encode('utf-8'))
                respuesta_dato = json.loads(s.recv(4096).decode('utf-8'))
                print(f"✅ Cliente {cliente_id}: Registro Dato: {respuesta_dato}")

            # 6. Consultar datos
            solicitud_consulta_datos = {"accion": "consultar_datos"}
            s.send(json.dumps(solicitud_consulta_datos).encode('utf-8'))
            respuesta_consulta_datos = json.loads(s.recv(4096).decode('utf-8'))
            
            datos_encontrados = respuesta_consulta_datos.get('data', {}).get('datos', [])
            print(f"✅ Cliente {cliente_id}: Encontrados {len(datos_encontrados)} datos")
            
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