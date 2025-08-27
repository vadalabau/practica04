# server.py
import socket
import threading
from database import SatelliteDatabase

db = SatelliteDatabase()

HOST = 'localhost'
PORT = 12345

def handle_client(conn, addr):
    print(f"Cliente conectado desde {addr}")
    while True:
        try:
            msg = conn.recv(4096).decode()
            if not msg:
                break

            if msg == "quit":
                break

            response = process_command(msg)
            conn.sendall(response.encode())

        except Exception as e:
            print(f"Error: {e}")
            break

    conn.close()
    print(f"Cliente desconectado {addr}")

def process_command(msg):
    try:
        cmd, *args = msg.split("|")
        cmd = cmd.upper()

        if cmd == "REGISTER_SATELLITE":
            sat_data = eval(args[0])
            db.add_satellite(sat_data)
            return "✅ Satélite registrado correctamente."

        elif cmd == "REGISTER_MISSION":
            mission_data = eval(args[0])
            db.add_mission(mission_data)
            return "✅ Misión registrada correctamente."

        elif cmd == "QUERY_SATELLITES":
            filtro = eval(args[0]) if args else None
            sats = db.get_satellites(filtro)
            return str(sats)

        elif cmd == "QUERY_MISSIONS":
            filtro = eval(args[0]) if args else None
            missions = db.get_missions(filtro)
            return str(missions)

        elif cmd == "REGISTER_DATA":
            data = eval(args[0])
            db.add_data(data)
            return "✅ Datos registrados correctamente."

        elif cmd == "QUERY_DATA":
            filtro = eval(args[0]) if args else None
            data = db.get_data(filtro)
            return str(data)

        else:
            return "❌ Comando no reconocido."

    except Exception as e:
        return f"❌ Error procesando comando: {e}"

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Servidor escuchando en {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()