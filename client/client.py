import socket
import json

HOST = "localhost"
PORT = 12345

def enviar_solicitud(accion, info=None):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORT))
    request = {"accion": accion, "info": info or {}}
    cliente.send(json.dumps(request).encode())
    respuesta = cliente.recv(8192).decode()
    cliente.close()
    return json.loads(respuesta)

def menu():
    while True:
        print("\nOpciones:")
        print("1. Registrar satélite")
        print("2. Consultar satélites")
        print("3. Registrar misión")
        print("4. Consultar misiones")
        print("5. Registrar dato de sensor")
        print("6. Consultar datos de sensores")
        print("7. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            info = {
                "nombre": input("Nombre: "),
                "tipo": input("Tipo: "),
                "sensores": input("Sensores (separados por coma): "),
                "fecha_lanzamiento": input("Fecha de lanzamiento (YYYY-MM-DD): "),
                "orbita": input("Órbita: "),
                "estado": input("Estado (activo/inactivo/en mantenimiento): ")
            }
            print(enviar_solicitud("registrar_satelite", info))
        elif opcion == "2":
            respuesta = enviar_solicitud("consultar_satelites")
            for s in respuesta.get("data", []):
                print(f"{s['id']}: {s['nombre']} ({s['tipo']}) - {s['estado']}")
        elif opcion == "3":
            info = {
                "satelite_id": int(input("ID del satélite: ")),
                "objetivo": input("Objetivo de la misión: "),
                "zona": input("Zona de observación: "),
                "duracion": input("Duración: "),
                "estado": input("Estado: ")
            }
            print(enviar_solicitud("registrar_mision", info))
        elif opcion == "4":
            respuesta = enviar_solicitud("consultar_misiones")
            for m in respuesta.get("data", []):
                print(f"{m['id']}: Satélite {m['satelite_id']} - {m['objetivo']} - {m['estado']}")
        elif opcion == "5":
            info = {
                "satelite_id": int(input("ID del satélite: ")),
                "tipo_dato": input("Tipo de dato: "),
                "valor": input("Valor: ")
            }
            print(enviar_solicitud("registrar_dato", info))
        elif opcion == "6":
            respuesta = enviar_solicitud("consultar_datos")
            for d in respuesta.get("data", []):
                print(f"{d['id']}: Satélite {d['satelite_id']} - {d['tipo_dato']} = {d['valor']}")
        elif opcion == "7":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()