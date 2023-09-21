import requests
import re
json_url1 = "https://github.com/pmayavi/IntroduccionAI_2023-2/raw/main/Development/Andres/comandos_difusos.json"
try:
    response = requests.get(json_url1)

    # Verifica si la descarga fue exitosa (código de respuesta 200)
    if response.status_code == 200:
        # El contenido del archivo JSON estará en response.json()
        data1 = response.json()

        print(data1)
    else:
        print(
            f"Error al descargar el archivo JSON. Código de respuesta: {response.status_code}"
        )

except Exception as e:
    print(f"Error: {e}")
base_conocimiento1 = []

for key, value in data1.items():
    for sin in value["palabras"]:
        base_conocimiento1.append((key, sin))


json_url2 = "https://github.com/pmayavi/IntroduccionAI_2023-2/raw/main/Development/Andres/difusos.json"
try:
    response = requests.get(json_url2)

    # Verifica si la descarga fue exitosa (código de respuesta 200)
    if response.status_code == 200:
        # El contenido del archivo JSON estará en response.json()
        data2 = response.json()

        print(data2)
    else:
        print(
            f"Error al descargar el archivo JSON. Código de respuesta: {response.status_code}"
        )
except Exception as e:
    print(f"Error: {e}")
base_conocimiento2 = []
for key, value in data2.items():
    for sin in value["palabras"]:
        base_conocimiento2.append((key, sin))

def enontrar_significado(texto,base_conocimiento):
    for comando, sin in base_conocimiento:
        # Buscar la primera ocurrencia del sinónimo en el texto
        match = re.search(r"\b{}\b".format(re.escape(sin)), texto, flags=re.IGNORECASE)
        if match:
            inicio_sinonimo, fin_sinonimo = match.start(), match.end()
            return (
                comando,
                sin,
                (inicio_sinonimo, fin_sinonimo)
            )
        
def mostrar_comando(texto):
    primer_resultado = enontrar_significado(texto,base_conocimiento1)
    segundo_resultado= enontrar_significado(texto,base_conocimiento2)
    if primer_resultado:
        if segundo_resultado:
            comando, sinonimo, posicion_sinonimo= primer_resultado
            difuso, sinonimo_difuso, posicion_difuso= segundo_resultado
            print(
                f"""
                Comando: {comando},
                Sinónimo: {sinonimo},
                Posición Sinónimo: ({posicion_sinonimo[0]}, {posicion_sinonimo[1]}),
                """
            )
            print(
                f"""
                Difuso: {difuso},
                Sinónimo: {sinonimo_difuso},
                Posición del difuso: ({posicion_difuso[0]}, {posicion_difuso[1]}),
                """
            )
            print(
                f"""
                Se hacen las acciones de [{data1[comando]['hacer'].replace('x', data2[difuso]['hacer'])}]
                """
            )
        else:
            print("No se encontraron resultados 2.")
    else:
        print("No se encontraron resultados.")

mostrar_comando("repite mas rápido lo que dijiste")