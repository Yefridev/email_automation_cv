from src.gmail.auth import obtener_servicio_gmail
from src.gmail.reader import obtener_correos_no_leidos

if __name__ == "__main__":
    servicio = obtener_servicio_gmail()
    correos = obtener_correos_no_leidos(servicio)

    for correo in correos:
        print("---")
        print("Asunto:", correo["asunto"])
        print("De:", correo["remitente"])