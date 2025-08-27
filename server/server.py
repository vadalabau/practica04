import socket
import threading
import json

# Archivos JSON para persistencia
SATELITES_FILE = "satelites.json"
MISIONES_FILE = "misiones.json"
DATOS_FILE = "datos.json"

# Cargar datos
def cargar_datos(ruta):
    try:
        with open(ruta, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_datos(ruta, data):
    with open(ruta, "w") as f:
        json.dump(data, f, indent=4)

# Funciones para manejar operaciones
def registrar_satelite(info):
    satelites = cargar_datos(SATELITES_FILE)
    nuevo_id = max([s["id"] for s in satelites], default=0) + 1
    info["id"] = nuevo_id
    info["sensores"] = [s.strip() for s in info.get("sensores", "").split(",")]
    satelites.append(info)
    guardar_datos(SATELITES_FILE, satelites)
    return {"status": "success", "message": "Satélite registrado"}

def consultar_satelites():
    satelites = cargar_datos(SATELITES_FILE)
    return {"status": "success", "data": satelites}

def registrar_mision(info):
    misiones = cargar_datos(MISIONES_FILE)
    nuevo_id = max([m["id"] for m in misiones], default=0) + 1
    info["id"] = nuevo_id
    misiones.append(info)
    guardar_datos(MISIONES_FILE, misiones)
    return {"status": "success", "message": "Misión registrada"}

def consultar_misiones():
    misiones = cargar_datos(MISIONES_FILE)
    return {"status": "success", "data": misiones}

def registrar_dato(info):
    datos = cargar_datos(DATOS_FILE)
    nuevo_id = max([d["id"] for d in datos], default=0) + 1
    info["id"] = nuevo_id
    datos.append(info)
    guardar_datos(DATOS_FILE, datos)
    return {"status": "success", "message": "Dato registrado"}

def consultar_datos():
    datos = cargar_datos(DATOS_FILE)
    return {"status": "success", "data": datos}

# Manejo de clientes
def manejar_cliente(conn, addr):
    print(f"Cliente conectado: {addr}")
    try:
        while True:
            data = conn.recv(4096).decode()
            if not data:
                break
            try:
                request = json.loads(data)
                accion = request.get("accion")
                info = request.get("info", {})
                if accion == "registrar_satelite":
                    respuesta = registrar_satelite(info)
                elif accion == "consultar_satelites":
                    respuesta = consultar_satelites()
                elif accion == "registrar_mision":
                    respuesta = registrar_mision(info)
                elif accion == "consultar_misiones":
                    respuesta = consultar_misiones()
                elif accion == "registrar_dato":
                    respuesta = registrar_dato(info)
                elif accion == "consultar_datos":
                    respuesta = consultar_datos()
                else:
                    respuesta = {"status": "error", "message": "Acción desconocida"}
            except Exception as e:
                respuesta = {"status": "error", "message": str(e)}
            conn.send(json.dumps(respuesta).encode())
    except Exception as e:
        print(f"Error con el cliente {addr}: {e}")
    finally:
        conn.close()
        print(f"Cliente desconectado: {addr}")

# Configuración del servidor
HOST = "localhost"
PORT = 12345
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print(f"Servidor escuchando en {HOST}:{PORT}")

while True:
    conn, addr = servidor.accept()
    threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()