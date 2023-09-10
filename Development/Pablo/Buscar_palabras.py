import json
import re
import pyttsx3

# Cargar el archivo JSON con la base de conocimientos, este esta en el
# [repositorio](https://github.com/pmayavi/IntroduccionAI_2023-2/raw/main/Development/Pablo/palabras.json)
import requests

json_url = "https://github.com/pmayavi/IntroduccionAI_2023-2/raw/main/Development/Pablo/palabras.json"
try:
    response = requests.get(json_url)

    # Verifica si la descarga fue exitosa (código de respuesta 200)
    if response.status_code == 200:
        # El contenido del archivo JSON estará en response.json()
        data = response.json()

        print(data)
    else:
        print(
            f"Error al descargar el archivo JSON. Código de respuesta: {response.status_code}"
        )

except Exception as e:
    print(f"Error: {e}")

# Crear una lista de sinónimos con información de su comando correspondiente
base_conocimiento = []
for key, value in data.items():
    for sin in value["palabras"]:
        base_conocimiento.append((key, sin))


# Encontrar el primer sinónimo en el texto
def enontrar_significado(texto):
    for comando, sin in base_conocimiento:
        # Buscar la primera ocurrencia del sinónimo en el texto
        match = re.search(r"\b{}\b".format(re.escape(sin)), texto, flags=re.IGNORECASE)
        if match:
            inicio_sinonimo, fin_sinonimo = match.start(), match.end()
            # Capturar los caracteres después del sinónimo hasta el final del texto
            caracteres_despues = texto[fin_sinonimo:]
            return (
                comando,
                sin,
                (inicio_sinonimo, fin_sinonimo),
                caracteres_despues.strip(),
            )


def mostrar_comando(texto):
    primer_resultado = enontrar_significado(texto)
    if primer_resultado:
        comando, sinonimo, posicion_sinonimo, contenido_despues = primer_resultado
        print(
            f"""
            Comando: {comando}, 
            Sinónimo: {sinonimo}, 
            Posición Sinónimo: ({posicion_sinonimo[0]}, {posicion_sinonimo[1]}), 
            Contenido despues del comando: {contenido_despues}
            """
        )
        print(
            f"""
            Se hacen las acciones de [{data[comando]['hacer'].replace('x', contenido_despues)}] 
            en la posicion de pantalla X:{data[comando]['ubicacion'][0]} Y:{data[comando]['ubicacion'][1]}
            """
        )
        # Decirlo en voz alta con voz en español
        engine = pyttsx3.init()
        engine.setProperty(
            "voice",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0",
        )
        engine.say(contenido_despues)
        engine.runAndWait()
    else:
        print("No se encontraron resultados.")


# Ejemplo de un string en el que buscar los comandos
mostrar_comando("Hola quiero investigar un resumen de la historia de los gatos")
