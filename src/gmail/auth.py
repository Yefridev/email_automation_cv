import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from loguru import logger



# Permisos que le pedimos a Gmail
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

RUTA_TOKEN = Path("token.json")
RUTA_CREDENCIALES = Path("credentials.json")

def obtener_servicio_gmail():
    
    credenciales = None

    #Si ya existe un token guardado, lo carga
    if RUTA_TOKEN.exists():
        credenciales = Credentials.from_authorized_user_file(
            str(RUTA_TOKEN), SCOPES
        )
        logger.info("Token existente cargado")
    
    #Si no hay credenciales válidas, inicia el flujo de login
    if not credenciales or not credenciales.valid:
        if credenciales and credenciales.expired and credenciales.refresh_token:
            logger.info("Token expirado, renovando ...")
            credenciales.refresh(Request())
        else:
            if not RUTA_CREDENCIALES.exists():
                raise FileNotFoundError(
                    "No se encontró credentials.json. "
                    "Descárgalo desde Google Cloud Console."
                )
            logger.info("Iniciando flujo de autenticación OAuth2...")
            flujo = InstalledAppFlow.from_client_secrets_file(
                str(RUTA_CREDENCIALES), SCOPES
            )
            credenciales = flujo.run_local_server(port=0)
        
        #Guarda el token para la proxima vez
        with open(RUTA_TOKEN, "w") as archivo_token:
            archivo_token.write(credenciales.to_json())
        logger.success("Token guardado en token.json")
    
    from googleapiclient.discovery import build
    servicio = build("gmail", "v1", credentials=credenciales)
    logger.success("Servicio Gmail listo")
    return servicio