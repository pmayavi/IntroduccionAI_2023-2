from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import defaultdict
import time
from selenium.common.exceptions import StaleElementReferenceException


# Inicializar el navegador Chrome
driver = webdriver.Chrome()

tiempo_inicio = time.time()
# Abrir la página web
driver.get("https://www.google.com")  # Reemplaza con la URL real

# Obtener todos los elementos de la página
elementos = driver.find_elements(By.XPATH, "//*")

# Crear un diccionario para almacenar los elementos por etiqueta
arbol_busqueda = defaultdict(list)
elements = []

# Clasificar los elementos por etiqueta
# Coger todos los elementos
for elemento in elementos:
    minutos, segundos = divmod(int(time.time() - tiempo_inicio), 60)
    print(f"Tiempo transcurrido: {minutos:02d}:{segundos:02d}", end="\r")
    etiqueta = elemento.tag_name
    elements.append(elemento)
    arbol_busqueda[etiqueta].append(elemento)

# Mostrar los elementos clasificados
# Cogiendo cosas de los elementos
prin = ""
ets = ""
elms = ""
ids = ""
for etiqueta, lista_elementos in arbol_busqueda.items():
    prin += f"\nElementos de la etiqueta '{etiqueta}':"
    ets += etiqueta + "\n"
    for elem in lista_elementos:
        minutos, segundos = divmod(int(time.time() - tiempo_inicio), 60)
        print(f"Tiempo transcurrido: {minutos:02d}:{segundos:02d}", end="\r")
        try:
            prin += f"- {elem.text.strip()}"  # Muestra el texto del elemento (puedes personalizar esto)
            elms += elem.text.strip()
            ids += elem.id
        except StaleElementReferenceException:
            print("Stale Element Reference Exception.")


print("\nRecorrido")
# Find the search bar element using different strategies
search_bar = None

# Buscando por elementos que tengan Search en su atributo texto
for element in elements:
    if "Search" in element.text:
        search_bar = element
        break

# If search bar is found, interact with it (e.g., send keys)
if search_bar:
    search_bar.send_keys("Search keyword")
else:
    print("no se encontro :(")

minutos, segundos = divmod(int(time.time() - tiempo_inicio), 60)
print(f"Tiempo transcurrido: {minutos:02d}:{segundos:02d}", end="\r")
# Cerrar el navegador

with open("all.txt", "w", encoding="utf-8") as file: #Elementos escritos en la pantalla, ya estructurados
    file.write(prin)

with open("elements.txt", "w", encoding="utf-8") as file: #Los elementos escritos en la pantalla sin estructura
    file.write(elms)

with open("ids.txt", "w", encoding="utf-8") as file: #Ilegible e innecesario
    file.write(ids)

with open("etiquetas.txt", "w", encoding="utf-8") as file: #Etiquetas de funciones
    file.write(ets)

minutos, segundos = divmod(int(time.time() - tiempo_inicio), 60)
print(f"Tiempo final: {minutos:02d}:{segundos:02d}", end="\r")

time.sleep(30)
driver.quit()
