from src.gmail.auth import obtener_servicio_gmail
from src.gmail.reader import obtener_correos_no_leidos
from src.classifier.engine import clasificar_correo

if __name__ == "__main__":
    servicio = obtener_servicio_gmail()
    correos = obtener_correos_no_leidos(servicio)

    for correo in correos:
        prioridad = clasificar_correo(correo)
        print("---")
        print("Asunto:", correo["asunto"])
        print("De:", correo["remitente"])
        print("Prioridad:", prioridad)