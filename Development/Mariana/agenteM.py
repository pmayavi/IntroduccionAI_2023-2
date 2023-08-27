from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Nodo:
    def __init__(self, elemento):
        self.elemento = elemento
        self.interactuable = False
        self.izquierda = None
        self.derecha = None

def insertar(nodo_actual, nuevo_elemento, es_interactuable):
    if nodo_actual is None:
        get_index(nuevo_elemento)
        nodo_nuevo = Nodo(nuevo_elemento)
        nodo_nuevo.interactuable = es_interactuable
        return nodo_nuevo
    
    get_index(nuevo_elemento)
    print("Nueva"+str(nuevo_elemento.i))
    print("Actual"+str(nodo_actual.elemento.i))

    if nuevo_elemento.i < nodo_actual.elemento.i:
        nodo_actual.izquierda = insertar(nodo_actual.izquierda, nuevo_elemento, es_interactuable)
    else:
        nodo_actual.derecha = insertar(nodo_actual.derecha, nuevo_elemento, es_interactuable)
    
    return nodo_actual

def get_index(elemento):
    if elemento.tag_name == "a":
        elemento.i=1
    elif elemento.tag_name == "button":
        elemento.i=2
    #elif elemento.tag_name == "menu":
    #    elemento.i=3
    #elif elemento.tag_name == "select":
    #    elemento.i=4
    elif elemento.tag_name == "input" or elemento.tag_name == "textarea":
        elemento.i=5
    else:
        elemento.i=0

def buscar_interactuable(nodo_actual, tag, i):
    if nodo_actual is None:
        return False
    
    if nodo_actual.elemento.tag_name == tag:
        return nodo_actual.elemento
    
    if i < nodo_actual.elemento.i:
        return buscar_interactuable(nodo_actual.izquierda, tag, i)
    else:
        return buscar_interactuable(nodo_actual.derecha, tag, i)

# Configuración de Selenium
driver = webdriver.Chrome()
url = "https://www.google.com"
driver.get(url)

# Obtener todas las elementos en la página
elementos = driver.find_elements(By.XPATH, "//*")

# Crear el nodo raíz del árbol
raiz = None

# Procesar las elementos
for elemento in elementos:
    es_interactuable = False
    
    # Aquí puedes agregar lógica para determinar si la elemento es interactuable
    # Por ejemplo, si es un enlace (<a>) o un botón (<button>)
    if elemento.tag_name in ["a", "button", "input", "textarea"]:
        es_interactuable = True
    
        raiz = insertar(raiz, elemento, es_interactuable)

# Buscar si una elemento específica es interactuable
elemento_buscada = "input"
es_interactuable = buscar_interactuable(raiz, elemento_buscada, 5)

if es_interactuable:
    print(f"El elemento <{elemento_buscad}> es interactuable.")
    # es_interactuable.send_keys("Search keyword")
else:
    print(f"El elemento <{elemento_buscada}> no es interactuable.")

# Cerrar el navegador
time.sleep(30)
driver.quit()
