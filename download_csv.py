import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json
import os

# Crear carpeta de descargas si no existe
download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
os.makedirs(download_dir, exist_ok=True)

# Configurar opciones de Chrome para descargas automáticas
options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True,
    "profile.default_content_setting_values.automatic_downloads": 1
})
options.add_argument("--start-maximized")

# Inicializar Chrome con las opciones y el servicio
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


def download_csv(driver, url):
    driver.get(url)
    sleep(5)  # Esperar 5 segundos para que cargue la página
    csvFileSel = "body > table > tbody > tr > td > table:nth-child(3) > tbody > tr:nth-child(1) > td > label > span.icon-file-excel > a"
    driver.find_element(By.CSS_SELECTOR, csvFileSel).click()
    sleep(10)  # Esperar 10 segundos para que el archivo se descargue


try:
    json_path = "./stations/stations_data.json"
    if not os.path.exists(json_path):
        raise FileNotFoundError(
            f"El archivo {json_path} no existe. Ejecuta primero scraping-mapeo.py."
        )

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            json_str = f.read()
            stations_data = json.loads(json_str)
            if not isinstance(stations_data, dict):
                print(f"Tipo actual de datos: {type(stations_data)}")
                raise TypeError("El JSON debe ser un diccionario en su nivel raíz")
        except json.JSONDecodeError as je:
            print(f"Formato JSON inválido: {je}")
            raise
except Exception as e:
    print(f"Error al procesar el archivo JSON: {e}")
    raise

try:
    xv_stations = stations_data.get("RI").get("stations")
    for station in xv_stations.values():
        for contaminant in station.get("contaminants").values():
            download_csv(driver, contaminant.get("graph_url"))

except FileNotFoundError as e:
    print(f"Archivo no encontrado: {e}")
except json.JSONDecodeError as e:
    print(f"Error al decodificar JSON: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    driver.quit()
