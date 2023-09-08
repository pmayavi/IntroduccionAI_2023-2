import json
import re

# Cargar el archivo JSON con los comandos y sus sinónimos
with open('palabras.json', 'r') as file:
    data = json.load(file)

# Ejemplo de un string en el que buscar los comandos
texto = "Este es un ejemplo que contiene palabra 1 y sinonimo3. También tiene palabra 2 con sinonimo6 que son diferentes."

# Crear una lista de sinónimos con información de su comando correspondiente
sinonimos_con_comando = []
for item in data:
    comando = item["comando"]
    sinonimos = item["palabras"]
    for sin in sinonimos:
        sinonimos_con_comando.append((comando, sin))

# Encontrar sinónimos en el texto
resultados = []

# Iniciar la posición de inicio del texto como 0
posicion_inicio = 0

for comando, sin in sinonimos_con_comando:
    # Buscar todas las ocurrencias del sinónimo en el texto
    matches = re.finditer(r'\b{}\b'.format(re.escape(sin)), texto, flags=re.IGNORECASE)
    for match in matches:
        inicio_sinonimo, fin_sinonimo = match.start(), match.end()
        # Agregar los caracteres después del sinónimo hasta el próximo comando o el final del texto
        #caracteres_despues = texto[posicion_inicio:inicio_sinonimo]  # Caracteres después del sinónimo
        resultados.append((comando, sin, (inicio_sinonimo, fin_sinonimo)))
        posicion_inicio = fin_sinonimo  # Actualizar la posición de inicio al final del sinónimo

for i in range(len(resultados)):
    elemento_actual = resultados[i]
    
    # Obtenemos el número 2 de la posición actual
    numero_2_actual = elemento_actual[2][1]
    
    if i == len(resultados) - 1:
        # Si es el último elemento, obtenemos el último caracter del string 'texto'
        numero_1_siguiente = len(texto) - 1
    else:
        # Obtenemos el número 1 de la siguiente posición
        siguiente_elemento = resultados[i + 1]
        numero_1_siguiente = siguiente_elemento[2][0]-1
    
    # Obtenemos los caracteres entre los dos números
    caracteres_entre_numeros = texto[numero_2_actual + 1:numero_1_siguiente + 1]
    
    # Agregamos los caracteres entre los números como un nuevo elemento en la lista 'resultados'
    resultados[i] = (elemento_actual[0], elemento_actual[1], (numero_2_actual, numero_1_siguiente), caracteres_entre_numeros)
    

for resultado in resultados:
    cont=0
    comando, sinonimo, posicion_sinonimo, contedido_despues= resultado
    print(f"Comando: {comando}, Sinónimo: {sinonimo}, Posición Sinónimo: ({posicion_sinonimo[0]}, {posicion_sinonimo[1]}), Contenido despues del comando: {contedido_despues}")
print ("hola")