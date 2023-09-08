import json
import re
import pyttsx3

# Cargar el archivo JSON con los comandos y sus sinónimos
with open("palabras.json", "r") as file:
    data = json.load(file)

# Ejemplo de un string en el que buscar los comandos
texto = "Hola quiero investigar un resumen de la historia de los gatos"

# Crear una lista de sinónimos con información de su comando correspondiente
sinonimos_con_comando = []
for item in data:
    comando = item["comando"]
    sinonimos = item["palabras"]
    for sin in sinonimos:
        sinonimos_con_comando.append((comando, sin))

# Encontrar el primer sinónimo en el texto
primer_resultado = None

for comando, sin in sinonimos_con_comando:
    # Buscar la primera ocurrencia del sinónimo en el texto
    match = re.search(r"\b{}\b".format(re.escape(sin)), texto, flags=re.IGNORECASE)
    if match:
        inicio_sinonimo, fin_sinonimo = match.start(), match.end()
        # Capturar los caracteres después del sinónimo hasta el final del texto
        caracteres_despues = texto[fin_sinonimo:]
        primer_resultado = (
            comando,
            sin,
            (inicio_sinonimo, fin_sinonimo),
            caracteres_despues,
        )
        break  # Detener la búsqueda después del primer match

if primer_resultado:
    comando, sinonimo, posicion_sinonimo, contenido_despues = primer_resultado
    print(
        f"Comando: {comando}, Sinónimo: {sinonimo}, Posición Sinónimo: ({posicion_sinonimo[0]}, {posicion_sinonimo[1]}), Contenido despues del comando: {contenido_despues}"
    )
    engine = pyttsx3.init()
    engine.setProperty(
        "voice",
        "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0",
    )
    engine.say(contenido_despues)
    engine.runAndWait()
else:
    print("No se encontraron resultados.")
