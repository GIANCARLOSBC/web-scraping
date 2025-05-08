from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from time import sleep

# Setup Firefox driver
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)
# URL generada en el paso anterior (scraping-mapeo.py)
url = "https://sinca.mma.gob.cl/cgi-bin/APUB-MMA/apub.htmlindico2.cgi?page=pageRight&header=Arica&gsize=1495x708&period=specified&from=000101&to=250506&macro=./RXV/F01/Cal/PM25//PM25.diario.anual.ic&limgfrom=&limgto=&limdfrom=&limdto=&rsrc=&stnkey="
driver.get(url)

# Ejecutando funcion Open para descargar archivo csv


def download_csv(driver, url):
    sleep(5)  # Esperar 5 segundos para que la página cargue completamente
    csvFileSel = "body > table > tbody > tr > td > table:nth-child(3) > tbody > tr:nth-child(1) > td > label > span.icon-file-excel > a"
    driver.find_element(By.CSS_SELECTOR, csvFileSel).click()
    sleep(10)  # Esperar 10 segundos para que el archivo se descargue


try:
    download_csv(driver, url)

except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the driver
    driver.quit()
