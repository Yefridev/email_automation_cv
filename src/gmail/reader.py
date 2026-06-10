from loguru import logger
from config.settings import MAX_EMAILS_PER_RUN

def obtener_correos_no_leidos(servicio):
    try:
        logger.info("Buscando correos no leídos...")

        #Busca los IDs de los correos no leídos
        resultado = servicio.users().messages().list(
            userId="me",
            q="is:unread in:inbox",
            maxResults=MAX_EMAILS_PER_RUN
        ).execute()

        mensajes = resultado.get("messages", [])

        if not mensajes:
            logger.info("No hay correos no leídos")
            return []
        
        logger.info(f"Encontrados {len(mensajes)} correos no leídos")

        correos = []
        for mensaje in mensajes:
            correo = _obtener_detalle_correo(servicio, mensaje["id"])
            if correo:
                correos.append(correo)

        return correos
    except Exception as error:
        logger.error(f"Error al obtener correos:{error}")
        return []
    
def _obtener_detalle_correo(servicio, id_mensaje):

    try: 
        mensaje = servicio.users().messages().get(
            userId="me",
            id=id_mensaje,
            format="full"
        ).execute()

        encabezados = mensaje["payload"]["headers"]

        #Extrae los campos importantes de los encabezados
        def obtener_encabezado(nombre):
            for encabezado in encabezados:
                if encabezado["name"].lower() == nombre.lower():
                    return encabezado["value"]
            return ""
        
        asunto = obtener_encabezado("Subject")
        remitente = obtener_encabezado("From")
        destinatario = obtener_encabezado("To")
        fecha = obtener_encabezado("Date")

        #Extrae el cuerpo del correo
        cuerpo = _extraer_cuerpo(mensaje["payload"])

        return{
            "id": id_mensaje,
            "asunto": asunto,
            "remitente": remitente,
            "destinatario": destinatario,
            "fecha": fecha,
            "cuerpo": cuerpo,
        }
    except Exception as error:
        logger.error(f"Error al obtener detalle del correo {id_mensaje}: {error}")
        return None
    
def _extraer_cuerpo(payload):

    import base64
    cuerpo = ""

    if "parts" in payload:
        for parte in payload["parts"]:
            if parte["mimeType"] == "text/plain":
                datos = parte["body"].get("data", "")
                if datos:
                    cuerpo = base64.urlsafe_b64decode(datos).decode("utf-8")
                    break
    else: 
        datos = payload["body"].get("data", "")
        if datos:
            cuerpo = base64.urlsafe_b64decode(datos).decode("utf-8")
    
    return cuerpo