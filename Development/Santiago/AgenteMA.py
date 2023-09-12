
# instalar PyAudio (pip install PyAudio)

keywords = set(
    [
        "Search",
        "search",
        "Búsqueda",
        "búsqueda",
        "busqueda",
        "Busqueda",
        "Buscar",
        "buscar",
    ]
)

peso = {
    "a_video": 1,
    "a_canal": 2,
    "a_feed": 3,
    "a_shorts": 4,
    "a_link": 5,
    "button": 6,
    "search_bar": 7,
    "input": 8,
    "textarea": 9,
}

class Nodo:
    def __init__(self, elemento):
        self.elemento = [elemento]
        self.interactuable = False
        self.izquierda = None
        self.derecha = None

    def imprimir_arbol(self, nivel=0):
        if self.derecha:
            self.derecha.imprimir_arbol(nivel + 1)
        
        # Agregar espacios para la indentación
        print("  " * nivel, end="")
        
        # Imprimir el elemento actual
        print(self.elemento[0]["Tagname"] + " " + str(len(self.elemento)) + " -> ")
        
        if self.izquierda:
            self.izquierda.imprimir_arbol(nivel + 1)


def insertar(nodo_actual, nuevo_elemento, es_interactuable):
    if nodo_actual is None:
        nodo_nuevo = Nodo(nuevo_elemento)
        nodo_nuevo.interactuable = es_interactuable
        return nodo_nuevo
    # print(nodo_actual)
    if nodo_actual.elemento[0] and nuevo_elemento["i"] < nodo_actual.elemento[0]["i"]:
        nodo_actual.izquierda = insertar(
            nodo_actual.izquierda, nuevo_elemento, es_interactuable
        )
    elif (
        nodo_actual.elemento[0]
        and nuevo_elemento["i"] == nodo_actual.elemento[0]["i"]
        and nuevo_elemento["Tagname"] == nodo_actual.elemento[0]["Tagname"]
    ):
        nodo_actual.elemento.append(nuevo_elemento)
    else:
        nodo_actual.derecha = insertar(
            nodo_actual.derecha, nuevo_elemento, es_interactuable
        )

    return nodo_actual

def get_index(elemento):
        tag = elemento["Tagname"]
        if tag == "a":  # si es link
            href = elemento["href"]
            text = elemento["text"]
            title = elemento["title"]

            if href and ("https://www.youtube.com" in href) and (text or title):
                if "https://www.youtube.com/watch" in href:  # es video?
                    elemento["i"] = peso["a_video"]
                elif (
                    "https://www.youtube.com/channel" in href
                    or "https://www.youtube.com/@" in href
                ):
                    elemento["i"] = peso["a_canal"]
                elif "https://www.youtube.com/feed" in href:
                    elemento["i"] = peso["a_feed"]
                elif "https://www.youtube.com/shorts" in href:
                    elemento["i"] = peso["a_shorts"]
                else:
                    elemento["i"] = peso["a_link"]
            else:
                elemento["i"] = 0
        elif tag == "button":
            elemento["i"] = peso["button"]
        elif validar_busqueda(elemento):
            elemento["i"] = peso["search_bar"]
        elif tag == "input":
            elemento["i"] = peso["input"]
        else:
            elemento["i"]= 0

def buscar_interactuable(nodo_actual, tag, i):
    if nodo_actual is None:
        return False

    if nodo_actual.elemento[0] and nodo_actual.elemento[0]["Tagname"] == tag:
        return nodo_actual

    if nodo_actual.elemento and i < nodo_actual.elemento[0]["i"]:
        return buscar_interactuable(nodo_actual.izquierda, tag, i)
    else:
        return buscar_interactuable(nodo_actual.derecha, tag, i)

def validar_busqueda(elemento):
    set2 = set(
        [
            elemento["label"],
            elemento["text"],
            elemento["HTML_id"],
            elemento["placeholder"],
        ]
    )
    common_elements = keywords.intersection(set2)
    return len(common_elements) > 0

'''
def create_json(elemento):
    new_element = {
    "Tagname": elemento["Tagname"],
    "href": elemento.get_attribute("href"),
    "text": elemento.get_attribute("title"),
    "tittle":elemento.text,
    "label":elemento.get_attribute("label"),
    "internal_id":elemento.id,
    "HTML_id":elemento.get_attribute("id"),
    "placeholder":elemento.get_attribute("placeholder")
    }
    return new_element
'''

import requests
def main():
    # Configuración de Selenium
    ##driver = webdriver.Chrome()
    ##url = "https://www.youtube.com"
    ## driver.get(url)
    #json_objects=[]
    #time.sleep(10)
    # Obtener todas las elementos en la página
    ## elementos = driver.find_elements(By.XPATH, "//*")
    # Crear el nodo raíz del árbol
    raiz = None
    all = ""

    # URL del archivo JSON en GitHub
    json_url = 'https://github.com/pmayavi/IntroduccionAI_2023-2/raw/main/Development/Santiago/archivo.json'

    try:
        response = requests.get(json_url)
    # Verifica si la descarga fue exitosa (código de respuesta 200)
        if response.status_code == 200:
        # El contenido del archivo JSON estará en response.json()
            data = response.json()
        else:
            print("Error al descargar el archivo JSON. Código de respuesta: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

    # Procesar los elementos del JSON Archivo
    for elemento in data:
        es_interactuable = False
        #json_objects.append(create_json(elemento))
        get_index(elemento)
        # Aquí puedes agregar lógica para determinar si la elemento es interactuable
        # Por ejemplo, si es un enlace (<a>) o un botón (<button>)
        if elemento["Tagname"] in [
            "a",
            "button",
            "input",
            "textarea",
        ] or validar_busqueda(elemento):
            es_interactuable = True
            raiz = insertar(raiz, elemento, es_interactuable)
            all += (
                elemento["Tagname"]
                + ": "
                + elemento["text"]
                + " "
                + str(elemento["i"])
                + "\n"
            )
        """
    with open("archivo.json", "w", encoding="utf-8") as json_file:
        json.dump(json_objects, json_file, indent=4)
    with open("./all.txt", "w", encoding="utf-8") as file:
        file.write(all)
        """
    # Imprimir el árbol en orden
    if raiz:
        print("Árbol:")
        raiz.imprimir_arbol()
    else:
        print("El árbol está vacío.")
    """
    # Buscar si una elemento específica es interactuable
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Di algo...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='es-ES')
            print("Dijiste: {}".format(text))
        except:
            print("¡Lo sentimos! No pudimos comprender los que dijiste")
    """
    text = input()
    splitted= text.split(' ', 1)
    comando= splitted[0] #INPUT POR VOZ EN CODIGO, POR TEXTO EN JUPYTER
    print("Comando: "+comando)
    elementos_busqueda=[]
    palabras_busqueda=splitted[1]
    print("Palabras: "+palabras_busqueda)

    if comando == "Buscar":
        elementos_busqueda=["ytd-searchbox", "searchbox", "textarea"]

    '''
    if comando == "Buscar":
        elementos_buscada=["ytd-searchbox", "searchbox", "textarea"]
    elif comando == "Regresar":
        ...
    '''

    #Para hacerlo genérico, va a buscar entre las etiquetas más comunes que tienen
    # las barras de búsqueda en HTML. Va a buscar en el árbol todos los elementos
    # de la lista hasta que encuentre uno que corresponda al peso 7 y que sea interactuable.
    es_interactuable=False
    for elemento in elementos_busqueda:
        elemento_busqueda = elemento
        es_interactuable = buscar_interactuable(raiz, elemento_busqueda, 7)
        if es_interactuable:
            break

    if es_interactuable:
        for elemento in es_interactuable.elemento:
            print(f"El elemento <{elemento_busqueda}> es interactuable.")
    else:
        print(f"El elemento <{elemento_busqueda}> no es interactuable.")

    # Cerrar el navegador
    ##driver.quit()

main()