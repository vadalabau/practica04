# server.py
import socket
import threading
import json
import sqlite3

DB_FILE = "sistema_satelites.db"
DATABASE_LOCK = threading.Lock()

# Inicializar la base de datos y crear tablas si no existen
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Tabla satelites
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS satelites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            tipo TEXT,
            sensores TEXT,
            fecha_lanzamiento TEXT,
            orbita TEXT,
            estado TEXT
        )
    ''')

    # Tabla misiones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS misiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            satelite_nombre TEXT,
            objetivo TEXT,
            zona TEXT,
            duracion INTEGER,
            estado TEXT,
            FOREIGN KEY (satelite_nombre) REFERENCES satelites(nombre)
        )
    ''')

    # Tabla datos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            satelite_nombre TEXT,
            tipo TEXT,
            valor TEXT,
            fecha TEXT,
            FOREIGN KEY (satelite_nombre) REFERENCES satelites(nombre)
        )
    ''')

    conn.commit()
    conn.close()

def handle_client(client_socket):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    while True:
        try:
            request = client_socket.recv(4096)
            if not request:
                break

            data = json.loads(request.decode())
            accion = data.get("accion")
            response = {"status": "error", "message": "Acción no reconocida"}

            if accion == "registrar_satelite":
                with DATABASE_LOCK:
                    try:
                        cursor.execute(
                            "INSERT INTO satelites (nombre,tipo,sensores,fecha_lanzamiento,orbita,estado) VALUES (?,?,?,?,?,?)",
                            (data["nombre"], data["tipo"], data["sensores"], data["fecha_lanzamiento"], data["orbita"], data["estado"])
                        )
                        conn.commit()
                        response = {"status": "success", "message": "Satélite registrado"}
                    except sqlite3.IntegrityError:
                        response = {"status": "error", "message": "El satélite ya existe"}

            elif accion == "consultar_satelites":
                with DATABASE_LOCK:
                    cursor.execute("SELECT * FROM satelites")
                    satelites = cursor.fetchall()
                    response = {"status": "success", "data": {"satelites": satelites}}

            elif accion == "registrar_mision":
                with DATABASE_LOCK:
                    cursor.execute("SELECT * FROM satelites WHERE nombre=?", (data["satelite_nombre"],))
                    if cursor.fetchone():
                        cursor.execute(
                            "INSERT INTO misiones (satelite_nombre,objetivo,zona,duracion,estado) VALUES (?,?,?,?,?)",
                            (data["satelite_nombre"], data["objetivo"], data["zona"], data["duracion"], data["estado"])
                        )
                        conn.commit()
                        response = {"status": "success", "message": "Misión registrada"}
                    else:
                        response = {"status": "error", "message": "Satélite no encontrado"}

            elif accion == "consultar_misiones":
                with DATABASE_LOCK:
                    cursor.execute("SELECT * FROM misiones")
                    misiones = cursor.fetchall()
                    response = {"status": "success", "data": {"misiones": misiones}}

            elif accion == "registrar_dato":
                with DATABASE_LOCK:
                    cursor.execute("SELECT * FROM satelites WHERE nombre=?", (data["satelite_nombre"],))
                    if cursor.fetchone():
                        cursor.execute(
                            "INSERT INTO datos (satelite_nombre,tipo,valor,fecha) VALUES (?,?,?,?)",
                            (data["satelite_nombre"], data["tipo"], data["valor"], data["fecha"])
                        )
                        conn.commit()
                        response = {"status": "success", "message": "Dato registrado"}
                    else:
                        response = {"status": "error", "message": "Satélite no encontrado"}

            elif accion == "consultar_datos":
                with DATABASE_LOCK:
                    cursor.execute("SELECT * FROM datos")
                    datos = cursor.fetchall()
                    response = {"status": "success", "data": {"datos": datos}}

            # Guardar backup
            with DATABASE_LOCK:
                cursor.execute("SELECT * FROM satelites")
                satelites = cursor.fetchall()
                cursor.execute("SELECT * FROM misiones")
                misiones = cursor.fetchall()
                cursor.execute("SELECT * FROM datos")
                datos = cursor.fetchall()
                with open("backup.json", "w") as f:
                    json.dump({"satelites": satelites, "misiones": misiones, "datos": datos}, f, indent=4)

            client_socket.send(json.dumps(response).encode())

        except Exception as e:
            client_socket.send(json.dumps({"status": "error", "message": str(e)}).encode())

    conn.close()
    client_socket.close()

def main():
    init_db()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen(5)
    print("Servidor escuchando en el puerto 12345...")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexión de {addr}")
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    main()