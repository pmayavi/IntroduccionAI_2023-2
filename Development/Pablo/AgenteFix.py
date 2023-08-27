from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import StaleElementReferenceException

tiempo_inicio = time.time()


def timer():
    minutos, segundos = divmod(int(time.time() - tiempo_inicio), 60)
    print(f"Tiempo transcurrido: {minutos:02d}:{segundos:02d}", end="\r")


# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the desired webpage
driver.get("https://www.youtube.com")


# Function to interact with an element and handle stale element exception
def interact_with_element(element):
    try:
        if element.tag_name == "input" and element.get_attribute("type") == "text":
            element.send_keys("Hello, Selenium!")
            elements.append(element)
    except StaleElementReferenceException:
        print("Stale Element Reference Exception.")


# Find all interactable elements on the page
interactable_elements = driver.find_elements(
    By.CSS_SELECTOR, '[onclick], [href], [type="button"], [type="submit"]'
)
timer()
elements = []

# Loop through the elements and interact with them
for element in interactable_elements:
    timer()
    interact_with_element(element)
    elements.append(element)

for element in elements:
    print(element.tag_name)

# Close the browser
print("Tiempo final")
time.sleep(30)
driver.quit()
