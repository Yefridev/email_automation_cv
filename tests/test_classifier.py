from src.classifier.engine import clasificar_correo


def test_correo_oferta_real_es_alta():
    correo = {
        "asunto": "Python Developer (Remote) en Hire Feed",
        "cuerpo": "Estamos buscando un desarrollador python junior",
        "remitente": "Alertas de empleo de LinkedIn <jobalerts-noreply@linkedin.com>",
    }
    assert clasificar_correo(correo) == "alta"


def test_correo_comercial_amazon_es_baja():
    correo = {
        "asunto": "Faltan 4 días para Prime Day",
        "cuerpo": "Explora preofertas y descuentos",
        "remitente": "Amazon Prime Day <store-news@amazon.com>",
    }
    assert clasificar_correo(correo) == "baja"


def test_correo_sin_palabras_clave_es_baja():
    correo = {
        "asunto": "Enviaste plata por Bre-B",
        "cuerpo": "Notificación de transferencia",
        "remitente": "notificaciones@nequi.com.co",
    }
    assert clasificar_correo(correo) == "baja"