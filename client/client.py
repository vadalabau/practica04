# client.py
import socket

HOST = 'localhost'
PORT = 12345

def send_command(sock, cmd):
    sock.sendall(cmd.encode())
    response = sock.recv(4096).decode()
    print(response)

def menu():
    print("\nOpciones:")
    print("1. Registrar satélite")
    print("2. Registrar misión")
    print("3. Consultar satélites")
    print("4. Consultar misiones")
    print("5. Registrar datos recolectados")
    print("6. Consultar datos recolectados")
    print("7. Salir")
    return input("Selecciona una opción (1-7): ")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print(f"✅ Conectado al servidor en {HOST}:{PORT}")

        while True:
            choice = menu()

            if choice == "1":
                sat = {
                    "nombre": input("Nombre: "),
                    "tipo": input("Tipo de satélite: "),
                    "sensores": input("Sensores (separados por coma): ").split(","),
                    "fecha_lanzamiento": input("Fecha de lanzamiento (YYYY-MM-DD): "),
                    "orbita": input("Órbita: "),
                    "estado": input("Estado (activo/inactivo/en mantenimiento): ")
                }
                send_command(sock, f"REGISTER_SATELLITE|{sat}")

            elif choice == "2":
                mission = {
                    "satellite": input("Satélite asignado: "),
                    "objetivo": input("Objetivo de la misión: "),
                    "zona": input("Zona de observación: "),
                    "duracion": input("Duración (en días): "),
                    "estado": input("Estado de la misión: ")
                }
                send_command(sock, f"REGISTER_MISSION|{mission}")

            elif choice == "3":
                filtro = input("Filtro opcional como diccionario (ej: {'estado':'activo'}), Enter para ninguno: ")
                filtro = filtro if filtro else None
                send_command(sock, f"QUERY_SATELLITES|{filtro}")

            elif choice == "4":
                filtro = input("Filtro opcional como diccionario (ej: {'estado':'en curso'}), Enter para ninguno: ")
                filtro = filtro if filtro else None
                send_command(sock, f"QUERY_MISSIONS|{filtro}")

            elif choice == "5":
                dato = {
                    "satellite": input("Satélite: "),
                    "tipo_dato": input("Tipo de dato: "),
                    "contenido": input("Contenido: ")
                }
                send_command(sock, f"REGISTER_DATA|{dato}")

            elif choice == "6":
                filtro = input("Filtro opcional como diccionario, Enter para ninguno: ")
                filtro = filtro if filtro else None
                send_command(sock, f"QUERY_DATA|{filtro}")

            elif choice == "7":
                send_command(sock, "quit")
                break

            else:
                print("Opción inválida.")

if __name__ == "__main__":
    main()