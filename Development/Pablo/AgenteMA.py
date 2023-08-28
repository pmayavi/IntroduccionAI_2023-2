from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import threading
import selenium.common.exceptions as ex
import speech_recognition as sr
# instalar PyAudio (pip install PyAudio)

set1 = set(
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
}


def auto_timmer():
    tiempo_inicio = time.time()

    def timer():
        while True:
            minutos, segundos = divmod(int(time.time() - tiempo_inicio), 60)
            print(
                f"                                                         Tiempo transcurrido: {minutos:02d}:{segundos:02d}",
                end="\r\r",
            )
            time.sleep(1)

    thread = threading.Thread(target=timer)
    thread.daemon = (
        True  # Set the thread as daemon so it will exit when the main program exits
    )
    thread.start()


class Nodo:
    def __init__(self, elemento):
        self.elemento = [elemento]
        self.interactuable = False
        self.izquierda = None
        self.derecha = None

    def imprimir_arbol(self):
        if self.izquierda:
            self.izquierda.imprimir_arbol()
        print(self.elemento[0].tag_name + " " + str(len(self.elemento)) + " -> ")
        if self.derecha:
            self.derecha.imprimir_arbol()


def insertar(nodo_actual, nuevo_elemento, es_interactuable):
    if nodo_actual is None:
        nodo_nuevo = Nodo(nuevo_elemento)
        nodo_nuevo.interactuable = es_interactuable
        return nodo_nuevo

    # print("Nueva"+str(nuevo_elemento.i))
    # print("Actual"+str(nodo_actual.elemento.i))

    try:
        # print(nodo_actual)
        if nodo_actual.elemento[0] and nuevo_elemento.i < nodo_actual.elemento[0].i:
            nodo_actual.izquierda = insertar(
                nodo_actual.izquierda, nuevo_elemento, es_interactuable
            )
        elif (
            nodo_actual.elemento[0]
            and nuevo_elemento.i == nodo_actual.elemento[0].i
            and nuevo_elemento.tag_name == nodo_actual.elemento[0].tag_name
        ):
            nodo_actual.elemento.append(nuevo_elemento)
        else:
            nodo_actual.derecha = insertar(
                nodo_actual.derecha, nuevo_elemento, es_interactuable
            )
    except ex.StaleElementReferenceException:
        print("Stale Element Reference Exception.")
        nodo_actual.derecha = insertar(
            nodo_actual.derecha, nuevo_elemento, es_interactuable
        )

    return nodo_actual


def get_index(elemento):
    try:
        tag = elemento.tag_name
        if tag == "a":  # si es link
            href = elemento.get_attribute("href")
            text = elemento.text
            title = elemento.get_attribute("title")

            if href and ("https://www.youtube.com" in href) and (text or title):
                if "https://www.youtube.com/watch" in href:  # es video?
                    elemento.i = peso["a_video"]
                elif (
                    "https://www.youtube.com/channel" in href
                    or "https://www.youtube.com/@" in href
                ):
                    elemento.i = peso["a_canal"]
                elif "https://www.youtube.com/feed" in href:
                    elemento.i = peso["a_feed"]
                elif "https://www.youtube.com/shorts" in href:
                    elemento.i = peso["a_shorts"]
                else:
                    elemento.i = peso["a_link"]
            else:
                elemento.i = 0
        elif tag == "button":
            elemento.i = peso["button"]
        elif validar_busqueda(elemento):
            elemento.i = peso["search_bar"]
        elif tag == "input":
            elemento.i = peso["input"]
        else:
            elemento.i = 0
    except ex.StaleElementReferenceException:
        print("Stale Element Reference Exception.")


def buscar_interactuable(nodo_actual, tag, i):
    if nodo_actual is None:
        return False

    if nodo_actual.elemento[0] and nodo_actual.elemento[0].tag_name == tag:
        return nodo_actual

    if nodo_actual.elemento and i < nodo_actual.elemento[0].i:
        return buscar_interactuable(nodo_actual.izquierda, tag, i)
    else:
        return buscar_interactuable(nodo_actual.derecha, tag, i)


def validar_busqueda(elemento):
    try:
        set2 = set(
            [
                elemento.get_attribute("label"),
                elemento.text,
                elemento.id,
                elemento.get_attribute("id"),
                elemento.get_attribute("placeholder"),
            ]
        )
        common_elements = set1.intersection(set2)
        return len(common_elements) > 0
    except ex.StaleElementReferenceException:
        print("Stale Element Reference Exception.")
        return False


def main():
    auto_timmer()
    # Configuración de Selenium
    driver = webdriver.Chrome()
    url = "https://www.youtube.com"
    driver.get(url)
    time.sleep(10)

    # Obtener todas las elementos en la página
    elementos = driver.find_elements(By.XPATH, "//*")

    # Crear el nodo raíz del árbol
    raiz = None
    all = ""

    # Procesar las elementos
    for elemento in elementos:
        es_interactuable = False
        get_index(elemento)

        # Aquí puedes agregar lógica para determinar si la elemento es interactuable
        # Por ejemplo, si es un enlace (<a>) o un botón (<button>)
        try:
            if elemento.tag_name in [
                "a",
                "button",
                "input",
                "textarea",
            ] or validar_busqueda(elemento):
                es_interactuable = True
                raiz = insertar(raiz, elemento, es_interactuable)
                all += (
                    elemento.tag_name
                    + ": "
                    + elemento.text
                    + " "
                    + str(elemento.i)
                    + "\n"
                )
        except ex.StaleElementReferenceException:
            print("Stale Element Reference Exception.")

    with open("./all.txt", "w", encoding="utf-8") as file:
        file.write(all)

    # Imprimir el árbol en orden
    if raiz:
        print("Árbol:")
        raiz.imprimir_arbol()
    else:
        print("El árbol está vacío.")

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

    comando="Buscar" #INPUT POR VOZ
    elementos_busqueda=[]
    palabras_busqueda="Funny cat videos"

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
            try:
                print(f"El elemento <{elemento_busqueda}> es interactuable.")
                elemento.send_keys(palabras_busqueda)
            except ex.ElementNotInteractableException:
                print("No es esta")
    else:
        print(f"El elemento <{elemento_busqueda}> no es interactuable.")

    # Cerrar el navegador
    time.sleep(30)
    driver.quit()


main()
