from src.gmail.auth import obtener_servicio_gmail

if __name__ == "__main__":
    servicio = obtener_servicio_gmail()
    print("Conexión exitosa con Gmail")