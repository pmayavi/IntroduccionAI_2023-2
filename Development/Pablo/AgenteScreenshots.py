import pyautogui
import pytesseract
from PIL import Image

# Ruta al ejecutable de Tesseract (puedes necesitar cambiarla)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_visible_images():
    # Captura de pantalla de la pantalla actual
    screenshot = pyautogui.screenshot()

    # Procesa la captura de pantalla usando Tesseract OCR
    extracted_text = pytesseract.image_to_string(screenshot)

    return extracted_text


# Extrae y muestra el texto de las imágenes visibles en la pantalla
extracted_text = extract_text_from_visible_images()
print(extracted_text)
