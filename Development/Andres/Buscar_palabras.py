import json
import re

# Cargar el archivo JSON con los comandos y sus sinónimos
with open('palabras.json', 'r') as file:
    data = json.load(file)

# Ejemplo de un string en el que buscar los comandos
texto = "Este es un ejemplo que contiene palabra 1 y sinonimo3. También tiene a sinonimo6."

# Crear una lista de sinónimos con información de su comando correspondiente
palabras_con_comando = []
for item in data:
    comando = item["comando"]
    palabras = item["palabras"]
    for sin in palabras:
        palabras_con_comando.append((comando, sin))

# Encontrar sinónimos en el texto
resultados = []

for comando, sin in palabras_con_comando:
    # Buscar todas las ocurrencias del sinónimo en el texto
    matches = re.finditer(r'\b{}\b'.format(re.escape(sin)), texto, flags=re.IGNORECASE)
    for match in matches:
        inicio_palabra, fin_palabra = match.start(), match.end()
        resultados.append((comando, sin, (inicio_palabra, fin_palabra)))

# Ordenar los resultados por posición en el texto
resultados.sort(key=lambda x: x[2])

# Imprimir los resultados
for resultado in resultados:
    comando, palabra, posicion_palabra = resultado
    print(f"Comando: {comando}, Palabra: {palabra}, Posición Palabra: ({posicion_palabra[0]}, {posicion_palabra[1]})")
