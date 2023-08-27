from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Nodo:
    def __init__(self, elemento):
        self.elemento = elemento
        self.interactuable = False
        self.izquierda = None
        self.derecha = None

    def imprimir_arbol(self):
        if self.izquierda:
            self.izquierda.imprimir_arbol()
        print(self.elemento.tag_name, end=" -> ")
        if self.derecha:
            self.derecha.imprimir_arbol()

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
    elif elemento.tag_name == "input":
        elemento.i=5
    elif elemento.tag_name == "ydt-searchbox" or validar_id_busqueda(elemento):
        elemento.i=6
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
    
def validar_id_busqueda(elemento):
    palabras_busqueda=["Search", "search", "Búsqueda", "búsqueda", "busqueda", "Busqueda", "Buscar", "buscar"]
    if elemento.id and any(palabra in str(elemento.id) for palabra in palabras_busqueda):
        return True
    else:
        return False
    
def validar_text_busqueda(elemento):
    palabras_busqueda=["Search", "search", "Búsqueda", "búsqueda", "busqueda", "Busqueda", "Buscar", "buscar"]
    if elemento.text and any(palabra in str(elemento.id) for palabra in palabras_busqueda):
        return True
    else:
        return False


# Configuración de Selenium
driver = webdriver.Chrome()
url = "https://www.youtube.com"
driver.get(url)

# Obtener todas las elementos en la página
elementos = driver.find_elements(By.XPATH, "//*")

# Crear el nodo raíz del árbol
raiz = None
all = ""

# Procesar las elementos
for elemento in elementos:
    es_interactuable = False
    
    # Aquí puedes agregar lógica para determinar si la elemento es interactuable
    # Por ejemplo, si es un enlace (<a>) o un botón (<button>)
    if validar_id_busqueda(elemento):
        es_interactuable = True
        raiz = insertar(raiz, elemento, es_interactuable)
        all += "Search: " + elemento.text + " " + elemento.id +  " "+ str(elemento.i) +"\n"
    elif validar_text_busqueda(elemento):
        es_interactuable = True
        raiz = insertar(raiz, elemento, es_interactuable)
        all += "Search: " + elemento.text + " " + elemento.id +  " "+ str(elemento.i) +"\n"
    elif elemento.tag_name in ["a", "button", "input", "textarea"]:
        es_interactuable = True
        raiz = insertar(raiz, elemento, es_interactuable)
        all += elemento.tag_name + ": " + elemento.text + " " + elemento.id + " "+ str(elemento.i) +"\n"
        

with open("./all.txt", "w", encoding="utf-8") as file:
    file.write(all)
    
# Imprimir el árbol en orden
if raiz:
    print("Árbol:")
    raiz.imprimir_arbol()
else:
    print("El árbol está vacío.")

# Buscar si una elemento específica es interactuable
elemento_buscada = "ydt-searchbox"
es_interactuable = buscar_interactuable(raiz, elemento_buscada, 5)

if es_interactuable:
    print(f"El elemento <{elemento_buscada}> es interactuable.")
    es_interactuable.send_keys("Tetas hombres")
else:
    print(f"El elemento <{elemento_buscada}> no es interactuable.")

# Cerrar el navegador
time.sleep(30)
driver.quit()
