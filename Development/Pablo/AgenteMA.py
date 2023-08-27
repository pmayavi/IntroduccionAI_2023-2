from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import threading
import selenium.common.exceptions as ex

def auto_timmer():
    tiempo_inicio = time.time()
    def timer():
        while True:
            minutos, segundos = divmod(int(time.time() - tiempo_inicio), 60)
            print(f"                                                         Tiempo transcurrido: {minutos:02d}:{segundos:02d}", end="\r\r")
            time.sleep(1)
    thread = threading.Thread(target=timer)
    thread.daemon = True  # Set the thread as daemon so it will exit when the main program exits
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
    
    #print("Nueva"+str(nuevo_elemento.i))
    #print("Actual"+str(nodo_actual.elemento.i))
    
    try:
        #print(nodo_actual)
        if nodo_actual.elemento[0] and nuevo_elemento.i < nodo_actual.elemento[0].i:
            nodo_actual.izquierda = insertar(nodo_actual.izquierda, nuevo_elemento, es_interactuable)
        elif nodo_actual.elemento[0] and nuevo_elemento.i == nodo_actual.elemento[0].i and nuevo_elemento.tag_name == nodo_actual.elemento[0].tag_name:
            nodo_actual.elemento.append(nuevo_elemento)
        else:
            nodo_actual.derecha = insertar(nodo_actual.derecha, nuevo_elemento, es_interactuable)
    except ex.StaleElementReferenceException:
        print("Stale Element Reference Exception.")
        nodo_actual.derecha = insertar(nodo_actual.derecha, nuevo_elemento, es_interactuable)

    return nodo_actual

def get_index(elemento):
    try:
        switch = {
            "a":1,
            "button":2,
            "input":3,
            "ydt-searchbox":4,
        }
        elemento.i = 0
        if elemento.tag_name in switch:
            elemento.i += switch[elemento.tag_name]
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
    set1 = set(["Search", "search", "Búsqueda", "búsqueda", "busqueda", "Busqueda", "Buscar", "buscar"])
    try:
        set2 = set([elemento.get_attribute("label"), elemento.text, elemento.id, elemento.get_attribute("id"), elemento.get_attribute("placeholder") ])
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
            if validar_busqueda(elemento):
                elemento.i = 4
                es_interactuable = True
                raiz = insertar(raiz, elemento, es_interactuable)
                all += "Search: " + elemento.text + " "+ str(elemento.i) +"\n"
            elif elemento.tag_name in ["a", "button", "input", "textarea"]:
                es_interactuable = True
                raiz = insertar(raiz, elemento, es_interactuable)
                all += elemento.tag_name + ": " + elemento.text + " "+ str(elemento.i) +"\n"
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
    elemento_buscada = "ytd-searchbox"
    es_interactuable = buscar_interactuable(raiz, elemento_buscada, 4)

    if es_interactuable:
        for elemento in es_interactuable.elemento:
            try:
                print(f"El elemento <{elemento_buscada}> es interactuable.")
                elemento.send_keys("Tetas hombres")
            except ex.ElementNotInteractableException:
                print("No es esta")
    else:
        print(f"El elemento <{elemento_buscada}> no es interactuable.")

    # Cerrar el navegador
    time.sleep(30)
    driver.quit()

main()