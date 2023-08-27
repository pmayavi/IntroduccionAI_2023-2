from selenium import webdriver

# Inicializar el controlador de Chrome
driver = webdriver.Chrome()

# Navegar a la página de resultados de búsqueda de YouTube
driver.get("https://www.youtube.com")

# Obtener todos los enlaces en la página
links = driver.find_elements(by="tag name", value="a")

# Crear archivos de texto para diferentes categorías
with open("videos.txt", "w", encoding="utf-8") as videos_file, \
     open("canales.txt", "w", encoding="utf-8") as canales_file, \
     open("feed.txt", "w", encoding="utf-8") as feed_file, \
     open("shorts.txt", "w", encoding="utf-8") as shorts_file, \
     open("demas_urls.txt", "w", encoding="utf-8") as demas_urls_file:
    
    canales_set = set()  # Para almacenar URLs de canales
    
    for link in links:
        href = link.get_attribute("href")
        text = link.text
        title = link.get_attribute("title")
        target = link.get_attribute("target")
        class_name = link.get_attribute("class")
        id_attr = link.get_attribute("id")
        
        if href:
            info = f"URL: {href}\nTexto: {text}\nTítulo: {title}\nTarget: {target}\nClase: {class_name}\nID: {id_attr}"
            info += "\n" + "-" * 30 + "\n"
            
            if "https://www.youtube.com/watch" in href:
                if text or title: #if para quitar los link de video sin descripción
                    videos_file.write(info)
            elif "https://www.youtube.com/channel" in href or "https://www.youtube.com/@" in href:
                # Verificar si el canal ya está en el set
                if href not in canales_set:# if para no repetir canales
                    canales_set.add(href)
                    canales_file.write(info)
            elif "https://www.youtube.com/feed" in href:
                if text or title: #if para quitar los link de video sin descripción
                    feed_file.write(info)
            elif "https://www.youtube.com/shorts" in href:
                shorts_file.write(info)
            else:
                demas_urls_file.write(info)
search_boxes = driver.find_elements(by="css selector", value="input[id='search']")
print("Barras de búsqueda encontradas:")
for search_box in search_boxes:
    search_name = search_box.get_attribute("name")
    search_id = search_box.get_attribute("id")
    print("Nombre de la barra de búsqueda:", search_name)
    print("ID de la barra de búsqueda:", search_id)
# Cerrar el navegador al finalizar
driver.quit()