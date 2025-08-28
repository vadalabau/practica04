# client.py
import socket
import json

def enviar_request(request):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 12345))
    client.send(json.dumps(request).encode())
    respuesta = client.recv(4096)
    client.close()
    return json.loads(respuesta.decode())

def menu():
    while True:
        print("\nOpciones:")
        print("1. Registrar satélite")
        print("2. Consultar satélites")
        print("3. Registrar misión")
        print("4. Consultar misiones")
        print("5. Registrar dato")
        print("6. Consultar datos")
        print("7. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            tipo = input("Tipo: ")
            sensores = input("Sensores: ")
            fecha_lanzamiento = input("Fecha de lanzamiento: ")
            orbita = input("Órbita: ")
            estado = input("Estado: ")
            request = {
                "accion": "registrar_satelite",
                "nombre": nombre,
                "tipo": tipo,
                "sensores": sensores,
                "fecha_lanzamiento": fecha_lanzamiento,
                "orbita": orbita,
                "estado": estado
            }
            print(enviar_request(request))

        elif opcion == "2":
            request = {"accion": "consultar_satelites"}
            respuesta = enviar_request(request)
            print(respuesta)

        elif opcion == "3":
            satelite_nombre = input("Nombre del satélite: ")
            objetivo = input("Objetivo: ")
            zona = input("Zona: ")
            duracion = int(input("Duración (días): "))
            estado = input("Estado: ")
            request = {
                "accion": "registrar_mision",
                "satelite_nombre": satelite_nombre,
                "objetivo": objetivo,
                "zona": zona,
                "duracion": duracion,
                "estado": estado
            }
            print(enviar_request(request))

        elif opcion == "4":
            request = {"accion": "consultar_misiones"}
            respuesta = enviar_request(request)
            print(respuesta)

        elif opcion == "5":
            satelite_nombre = input("Nombre del satélite: ")
            tipo = input("Tipo de dato: ")
            valor = input("Valor: ")
            fecha = input("Fecha: ")
            request = {
                "accion": "registrar_dato",
                "satelite_nombre": satelite_nombre,
                "tipo": tipo,
                "valor": valor,
                "fecha": fecha
            }
            print(enviar_request(request))

        elif opcion == "6":
            request = {"accion": "consultar_datos"}
            respuesta = enviar_request(request)
            print(respuesta)

        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()