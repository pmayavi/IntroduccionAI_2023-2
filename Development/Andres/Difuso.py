import requests
import re


def getJSON(json_url):
    try:
        response = requests.get(json_url)
        # Verifica si la descarga fue exitosa (código de respuesta 200)
        if response.status_code == 200:
            # El contenido del archivo JSON estará en response.json()
            data = response.json()
        else:
            print(f"Error al descargar el archivo JSON: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")
    base_conocimiento = []

    for key, value in data.items():
        for sin in value["palabras"]:
            base_conocimiento.append((key, sin))

    return base_conocimiento, data


base_conocimiento1, data1 = getJSON(
    "https://github.com/pmayavi/IntroduccionAI_2023-2/raw/main/Development/Andres/comandos_difusos.json"
)
base_conocimiento2, data2 = getJSON(
    "https://github.com/pmayavi/IntroduccionAI_2023-2/raw/main/Development/Andres/difusos.json"
)


def enontrar_significado(texto, base_conocimiento):
    for comando, sin in base_conocimiento:
        # Buscar la primera ocurrencia del sinónimo en el texto
        match = re.search(r"\b{}\b".format(re.escape(sin)), texto, flags=re.IGNORECASE)
        if match:
            inicio_sinonimo, fin_sinonimo = match.start(), match.end()
            return (comando, sin, (inicio_sinonimo, fin_sinonimo))


def mostrar_comando(texto):
    primer_resultado = enontrar_significado(texto, base_conocimiento1)
    segundo_resultado = enontrar_significado(texto, base_conocimiento2)
    if primer_resultado:
        if segundo_resultado:
            comando, sinonimo, posicion_sinonimo = primer_resultado
            difuso, sinonimo_difuso, posicion_difuso = segundo_resultado
            print(
                f"""
                Comando detectado: {comando},
                Posición Sinónimo: ({posicion_sinonimo[0]}, {posicion_sinonimo[1]}),
                Comando difuso detectado: {difuso},
                Posición del difuso: ({posicion_difuso[0]}, {posicion_difuso[1]}),
                Se hace la accion de [{data1[comando]['hacer'].replace('x', data2[difuso]['hacer'])}]
                """
            )
        else:
            print("No se encontraron resultados 2.")
    else:
        print("No se encontraron resultados.")


mostrar_comando("repite mas rápido lo que dijiste")
