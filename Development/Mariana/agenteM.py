from selenium import webdriver
from selenium.webdriver.common.by import By

class Nodo:
    def __init__(self, etiqueta):
        self.etiqueta = etiqueta
        self.interactuable = False
        self.izquierda = None
        self.derecha = None

def insertar(nodo_actual, nueva_etiqueta, es_interactuable):
    if nodo_actual is None:
        nodo_nuevo = Nodo(nueva_etiqueta)
        nodo_nuevo.interactuable = es_interactuable
        return nodo_nuevo
    
    get_index(nueva_etiqueta)
    get_index(nodo_actual.etiqueta)
    print("Nueva"+str(nueva_etiqueta.i))
    print("Actual"+str(nodo_actual.i))

    if nueva_etiqueta.i < nodo_actual.i:
        nodo_actual.izquierda = insertar(nodo_actual.izquierda, nueva_etiqueta, es_interactuable)
    else:
        nodo_actual.derecha = insertar(nodo_actual.derecha, nueva_etiqueta, es_interactuable)
    
    return nodo_actual

def get_index(etiqueta):
    if etiqueta.tag_name == "a":
        etiqueta.i=1
    elif etiqueta.tag_name == "button":
        etiqueta.i=2
    #elif etiqueta.tag_name == "menu":
    #    etiqueta.i=3
    #elif etiqueta.tag_name == "select":
    #    etiqueta.i=4
    elif etiqueta.tag_name == "input" or etiqueta.tag_name == "textarea":
        etiqueta.i=5
    else:
        etiqueta.i=0

def buscar_interactuable(nodo_actual, etiqueta):
    if nodo_actual is None:
        return False
    
    if nodo_actual.etiqueta == etiqueta:
        return nodo_actual.interactuable
    
    get_index(etiqueta)
    if etiqueta.i < nodo_actual.etiqueta.i:
        return buscar_interactuable(nodo_actual.izquierda, etiqueta)
    else:
        return buscar_interactuable(nodo_actual.derecha, etiqueta)

# Configuración de Selenium
driver = webdriver.Chrome()
url = "https://www.google.com"
driver.get(url)

# Obtener todas las etiquetas en la página
etiquetas = driver.find_elements(By.XPATH, "//*")

# Crear el nodo raíz del árbol
raiz = None

# Procesar las etiquetas
for etiqueta in etiquetas:
    es_interactuable = False
    
    # Aquí puedes agregar lógica para determinar si la etiqueta es interactuable
    # Por ejemplo, si es un enlace (<a>) o un botón (<button>)
    if etiqueta.tag_name in ["a", "button", "input", "textarea"]:
        es_interactuable = True
    
    raiz = insertar(raiz, etiqueta.tag_name, es_interactuable)

# Buscar si una etiqueta específica es interactuable
etiqueta_buscada = "input"
es_interactuable = buscar_interactuable(raiz, etiqueta_buscada)

if es_interactuable:
    print(f"La etiqueta <{etiqueta_buscada}> es interactuable.")
else:
    print(f"La etiqueta <{etiqueta_buscada}> no es interactuable.")

# Cerrar el navegador
driver.quit()
