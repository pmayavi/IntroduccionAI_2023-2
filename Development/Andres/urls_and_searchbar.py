from selenium import webdriver
import webbrowser

# Inicializar el controlador de Chrome
driver = webdriver.Chrome()

# Navegar a la página de resultados de búsqueda de YouTube
driver.get("https://www.youtube.com")
while True:
    accion = input("Quieres buscar algo o quieres ver recomendados (buscar/recomendados)").lower()
    if accion=="recomendados":
        # Obtener todos los enlaces en la página
        links = driver.find_elements(by="tag name", value="a")

        # Crear archivos de texto para diferentes categorías
        with open("videos.txt", "w", encoding="utf-8") as videos_file, \
            open("canales.txt", "w", encoding="utf-8") as canales_file, \
            open("feed.txt", "w", encoding="utf-8") as feed_file, \
            open("shorts.txt", "w", encoding="utf-8") as shorts_file, \
            open("demas_urls.txt", "w", encoding="utf-8") as demas_urls_file:
            
            canales_set = set()  # Para almacenar URLs de canales
            video_list = []  # Lista de tuplas de videos con título/texto y URL
            canales_list = []  # Lista de tuplas de canales con título/texto y URL
            feed_list = []  # Lista de tuplas de feeds con título/texto y URL
            shorts_list = []  # Lista de tuplas de shorts con título/texto y URL
            
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
                        if text or title:
                            videos_file.write(info)
                            video_list.append((text or title, href))
                    elif "https://www.youtube.com/channel" in href or "https://www.youtube.com/@" in href:
                        if href not in canales_set:
                            canales_set.add(href)
                            canales_file.write(info)
                            canales_list.append((text or title, href))
                    elif "https://www.youtube.com/feed" in href:
                        if text or title:
                            feed_file.write(info)
                            feed_list.append((text or title, href))
                    elif "https://www.youtube.com/shorts" in href:
                        shorts_file.write(info)
                        shorts_list.append((text or title, href))
                    else:
                        demas_urls_file.write(info)

        # Preguntar al usuario qué lista imprimir y abrir un enlace asociado
        lista_a_imprimir = input("¿Qué lista deseas imprimir? (videos/canales/feed/shorts): ").lower()

        if lista_a_imprimir in ["videos", "canales", "feed", "shorts"]:
                if lista_a_imprimir == "videos":
                    print("Lista de videos con título/texto y URL:")
                    for index, (title_text, href) in enumerate(video_list, start=1):
                        print(f"{index}. {title_text}")
                    opcion = input("¿Prefieres dar el nombre o el número de la opción? ").lower()
                    if opcion == "nombre":
                        titulo_seleccionado = input("Ingrese el título del video que desea abrir: ")
                        for title_text, link in video_list:
                            if titulo_seleccionado.lower() in title_text.lower():
                                driver.get(link)
                                break
                    elif opcion == "numero":
                        index = int(input("Seleccione el número del video para abrir: ")) - 1
                        if 0 <= index < len(video_list):
                            driver.get(video_list[index][1])
                        else:
                            print("Número de opción no válido")
                    else:
                        print("Opción no válida")
                elif lista_a_imprimir == "canales":
                    print("Lista de canales con título/texto y URL:")
                    for title_text, href in canales_list:
                        print(title_text)
                    opcion = input("¿Prefieres dar el nombre o el número de la opción? ").lower()
                    if opcion == "nombre":
                        titulo_seleccionado = input("Ingrese el título del canal que desea abrir: ")
                        for title_text, link in canales_list:
                            if titulo_seleccionado.lower() in title_text.lower():
                                driver.get(link)
                                break
                    elif opcion == "numero":
                        index = int(input("Seleccione el número del canal para abrir: ")) - 1
                        if 0 <= index < len(canales_list):
                            driver.get(canales_list[index][1])
                        else:
                            print("Número de opción no válido")
                    else:
                        print("Opción no válida")
                elif lista_a_imprimir == "feed":
                    print("Lista de feeds con título/texto y URL:")
                    for title_text, href in feed_list:
                        print(title_text)
                    opcion = input("¿Prefieres dar el nombre o el número de la opción? ").lower()
                    if opcion == "nombre":
                        titulo_seleccionado = input("Ingrese el título del feed que desea abrir: ")
                        for title_text, link in feed_list:
                            if titulo_seleccionado.lower() in title_text.lower():
                                driver.get(link)
                                break
                    elif opcion == "numero":
                        index = int(input("Seleccione el número del feed para abrir: ")) - 1
                        if 0 <= index < len(feed_list):
                            driver.get(feed_list[index][1])
                        else:
                            print("Número de opción no válido")
                    else:
                        print("Opción no válida")
                elif lista_a_imprimir == "shorts":
                    print("Lista de shorts con título/texto y URL:")
                    for title_text, href in shorts_list:
                        print(title_text)
                    opcion = input("¿Prefieres dar el nombre o el número de la opción? ").lower()
                    if opcion == "nombre":
                        titulo_seleccionado = input("Ingrese el título del short que desea abrir: ")
                        for title_text, link in shorts_list:
                            if titulo_seleccionado.lower() in title_text.lower():
                                driver.get(link)
                                break
                    elif opcion == "numero":
                        index = int(input("Seleccione el número del short para abrir: ")) - 1
                        if 0 <= index < len(shorts_list):
                            driver.get(str(shorts_list[index][1]))
                        else:
                            print("Número de opción no válido")
                    else:
                        print("Opción no válida")
        else:
            print("Lista no reconocida")
    elif accion == "buscar":
        # Obtener todas las barras de búsqueda utilizando un selector CSS como solo hay una en pagina principal se queda es con esa
        driver.get("https://www.youtube.com")
        search_boxes = driver.find_elements(by="css selector", value="input[id='search']")
        print("Barras de búsqueda encontradas:")
        for search_box in search_boxes:
            search_name = search_box.get_attribute("name")
            search_id = search_box.get_attribute("id")
            print("Nombre de la barra de búsqueda:", search_name)
            print("ID de la barra de búsqueda:", search_id)
        texto=input("Que quires buscar?")
        search_box.clear()
        search_box.send_keys(texto)
        search_box.submit() 
        driver.get(driver.current_url)
        links = driver.find_elements(by="tag name", value="a")
        # Crear archivos de texto para diferentes categorías
        with open("videos.txt", "w", encoding="utf-8") as videos_file, \
            open("canales.txt", "w", encoding="utf-8") as canales_file, \
            open("feed.txt", "w", encoding="utf-8") as feed_file, \
            open("shorts.txt", "w", encoding="utf-8") as shorts_file, \
            open("demas_urls.txt", "w", encoding="utf-8") as demas_urls_file:
            
            canales_set = set()  # Para almacenar URLs de canales
            video_list = []  # Lista de tuplas de videos con título/texto y URL
            canales_list = []  # Lista de tuplas de canales con título/texto y URL
            feed_list = []  # Lista de tuplas de feeds con título/texto y URL
            shorts_list = []  # Lista de tuplas de shorts con título/texto y URL
            
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
                        if text or title:
                            videos_file.write(info)
                            video_list.append((text or title, href))
                    elif "https://www.youtube.com/channel" in href or "https://www.youtube.com/@" in href:
                        if href not in canales_set:
                            canales_set.add(href)
                            canales_file.write(info)
                            canales_list.append((text or title, href))
                    elif "https://www.youtube.com/feed" in href:
                        if text or title:
                            feed_file.write(info)
                            feed_list.append((text or title, href))
                    elif "https://www.youtube.com/shorts" in href:
                        shorts_file.write(info)
                        shorts_list.append((text or title, href))
                    else:
                        demas_urls_file.write(info)

        # Preguntar al usuario qué lista imprimir y abrir un enlace asociado
        lista_a_imprimir = input("¿Qué lista deseas imprimir? (videos/canales/feed/shorts): ").lower()

        if lista_a_imprimir in ["videos", "canales", "feed", "shorts"]:
                if lista_a_imprimir == "videos":
                    print("Lista de videos con título/texto y URL:")
                    for index, (title_text, href) in enumerate(video_list, start=1):
                        print(f"{index}. {title_text}")
                    opcion = input("¿Prefieres dar el nombre o el número de la opción? ").lower()
                    if opcion == "nombre":
                        titulo_seleccionado = input("Ingrese el título del video que desea abrir: ")
                        for title_text, link in video_list:
                            if titulo_seleccionado.lower() in title_text.lower():
                                driver.get(link)
                                break
                    elif opcion == "numero":
                        index = int(input("Seleccione el número del video para abrir: ")) - 1
                        if 0 <= index < len(video_list):
                            driver.get(video_list[index][1])
                        else:
                            print("Número de opción no válido")
                    else:
                        print("Opción no válida")
                elif lista_a_imprimir == "canales":
                    print("Lista de canales con título/texto y URL:")
                    for title_text, href in canales_list:
                        print(title_text)
                    opcion = input("¿Prefieres dar el nombre o el número de la opción? ").lower()
                    if opcion == "nombre":
                        titulo_seleccionado = input("Ingrese el título del canal que desea abrir: ")
                        for title_text, link in canales_list:
                            if titulo_seleccionado.lower() in title_text.lower():
                                driver.get(link)
                                break
                    elif opcion == "numero":
                        index = int(input("Seleccione el número del canal para abrir: ")) - 1
                        if 0 <= index < len(canales_list):
                            driver.get(canales_list[index][1])
                        else:
                            print("Número de opción no válido")
                    else:
                        print("Opción no válida")
                elif lista_a_imprimir == "feed":
                    print("Lista de feeds con título/texto y URL:")
                    for title_text, href in feed_list:
                        print(title_text)
                    opcion = input("¿Prefieres dar el nombre o el número de la opción? ").lower()
                    if opcion == "nombre":
                        titulo_seleccionado = input("Ingrese el título del feed que desea abrir: ")
                        for title_text, link in feed_list:
                            if titulo_seleccionado.lower() in title_text.lower():
                                driver.get(link)
                                break
                    elif opcion == "numero":
                        index = int(input("Seleccione el número del feed para abrir: ")) - 1
                        if 0 <= index < len(feed_list):
                            driver.get(feed_list[index][1])
                        else:
                            print("Número de opción no válido")
                    else:
                        print("Opción no válida")
                elif lista_a_imprimir == "shorts":
                    print("Lista de shorts con título/texto y URL:")
                    for title_text, href in shorts_list:
                        print(title_text)
                    opcion = input("¿Prefieres dar el nombre o el número de la opción? ").lower()
                    if opcion == "nombre":
                        titulo_seleccionado = input("Ingrese el título del short que desea abrir: ")
                        for title_text, link in shorts_list:
                            if titulo_seleccionado.lower() in title_text.lower():
                                driver.get(link)
                                break
                    elif opcion == "numero":
                        index = int(input("Seleccione el número del short para abrir: ")) - 1
                        if 0 <= index < len(shorts_list):
                            driver.get(str(shorts_list[index][1]))
                        else:
                            print("Número de opción no válido")
                    else:
                        print("Opción no válida")
        else:
            print("Lista no reconocida")
    else:
        print("Accion no reconocida")


    # Cerrar el navegador al finalizar
    #driver.quit()
