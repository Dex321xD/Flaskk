from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

def obtener_precio_cobre():
    url = 'https://es.investing.com/commodities/copper'

    # Configuración del navegador
    options = Options()
    options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Para evitar errores en contenedores
    options.add_argument("--remote-debugging-port=9222")

    # Inicializar el controlador del navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(3)  # Esperar para asegurar la carga de la página

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="instrument-price-last"]'))
        )

        # Extraer el precio del cobre
        precio_element = driver.find_element(By.CSS_SELECTOR, 'div[data-test="instrument-price-last"]')
        precio_cobre = precio_element.text

        return precio_cobre
    except Exception as e:
        return f"Error al obtener el precio del cobre: {e}"
    finally:
        driver.quit()

@app.route('/api/obtener_precio_cobre', methods=['GET'])
def api_obtener_precio_cobre():
    precio = obtener_precio_cobre()
    return jsonify({'precio_cobre': precio})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
