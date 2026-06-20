import re
from loguru import logger

DOMINIOS_EXCLUIDOS = [
    "amazon.com", "samsung.com", "coursera.org", "cinemark.com.co",
    "duolingo.com", "nequi.com.co", "apple.com", "skills.google.com"
]

PALABRAS_ALTA_PRIORIDAD = [
    "oferta", "vacante", "entrevista", "proceso de selección",
    "python developer", "desarrollador python", "backend developer",
    "junior developer", "estamos interesados", "tu perfil",
]

PALABRA_MEDIA_PRIORIDAD = [
    "linkedin", "reclutador", "recursos humanos", "talet acquisition",
    "oportunidad laboral", "nos gustaría conocerte",
]

PALABRAS_BAJA_PRIORIDAD = [
    "newsletter", "boletín", "no-reply",
    "unsubscribe", "darse de baja", "promoción"
]


def clasificar_correo(correo):
    

    remitente = correo["remitente"].lower()

    # Si el remitente es un dominio comercial conocido, nunca es alta

    if any(dominio in remitente for dominio in DOMINIOS_EXCLUIDOS):
        logger.info(f"Correo '{correo['asunto'][:40]}...' excluido por dominio: baja")
        return "baja"

    #Recibe un correo y retorna su prioridad

    texto_completo = f"{correo['asunto']} {correo['cuerpo']}".lower()

    if _contiene_alguna(texto_completo, PALABRAS_ALTA_PRIORIDAD):
        prioridad = "alta"
    elif _contiene_alguna(texto_completo, PALABRA_MEDIA_PRIORIDAD):
        prioridad = "media"
    else:
        prioridad = "baja"
    
    logger.info(f"Correo '{correo['asunto'][:40]}...' clasificado como: {prioridad}")
    return prioridad

def _contiene_alguna(texto, lista_palabras):

    # Revisa si alguna palabra de la lista aparece dentro del texto.
    for palabra in lista_palabras:
        patron = r"\b" + re.escape(palabra) + r"\b"
        if re.search(patron, texto):
            return True
    return False
