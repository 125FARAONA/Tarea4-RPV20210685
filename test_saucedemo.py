import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

lista_capturas = []

def iniciar_driver():
    opciones = Options()
    opciones.add_argument("--start-maximized")
    servicio = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servicio, options=opciones)
    return driver

def iniciar_sesion(driver, usuario, contrasena):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(usuario)
    driver.find_element(By.ID, "password").send_keys(contrasena)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    tomar_captura(driver, "login_exitoso.png")

def agregar_producto_al_carrito(driver):
    driver.find_elements(By.CLASS_NAME, "inventory_item")[0].click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "btn_inventory").click()
    time.sleep(1)
    tomar_captura(driver, "producto_agregado.png")

def verificar_producto_en_carrito(driver):
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(2)
    productos = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(productos) > 0, "No hay productos en el carrito"
    print(f"Productos en el carrito: {len(productos)}")
    tomar_captura(driver, "productos_en_carrito.png")

def eliminar_producto_del_carrito(driver):
    driver.find_element(By.CLASS_NAME, "cart_button").click()
    time.sleep(1)
    tomar_captura(driver, "producto_eliminado.png")

def verificar_carrito_vacio(driver):
    productos = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(productos) == 0, "El carrito NO está vacío"
    print("El carrito está vacío")
    tomar_captura(driver, "carrito_vacio.png")

def tomar_captura(driver, nombre_archivo):
    ruta = os.path.join(os.getcwd(), "screenshots")
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    path_completo = os.path.join(ruta, nombre_archivo)
    driver.save_screenshot(path_completo)
    lista_capturas.append(path_completo)
    print(f"[Captura] {nombre_archivo} guardada")

def crear_reporte():
    contenido = """
    <html>
    <head>
        <title>Reporte de Pruebas Automatizadas - Saucedemo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1, h2, h3 { color: #2E86C1; }
            img { border: 1px solid #ddd; margin-bottom: 15px; }
            .info { margin-bottom: 30px; }
            hr { border: none; border-top: 1px solid #ccc; margin: 40px 0; }
        </style>
    </head>
    <body>
        <h1>Reporte de Pruebas Automatizadas - Saucedemo</h1>
        <div class="info">
            <p><strong>Hecho por:</strong> Rozenny P. Valentin / 2021-0685</p>
            <p><strong>Materia:</strong> Programación 3</p>
            <p><strong>Tarea:</strong> Tarea 4 - Pruebas Automatizadas con Selenium</p>
            <p><strong>Repositorios y enlaces:</strong><br>
                <a href="https://github.com/125FARAONA/Tarea4-RPV20210685" target="_blank">GitHub</a> | 
                <a href="https://1drv.ms/f/c/dce57cf10bc7ec63/EiIjgfhMajxClVDVwbNj5lIBvPeZPbUfADnvp5_ZZlK0yg?e=4W7NBZ" target="_blank">OneDrive</a> | 
                <a href="https://rozennyv.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog" target="_blank">Jira</a>
            </p>
        </div>
    """

    for captura in lista_capturas:
        nombre = os.path.basename(captura)
        contenido += f'<div><h3>{nombre}</h3><img src="screenshots/{nombre}" width="600"></div><hr>'

    contenido += """
    </body>
    </html>
    """

    with open("reporte.html", "w", encoding="utf-8") as f:
        f.write(contenido)

    print("[Reporte] reporte.html creado")


def cerrar_driver(driver):
    driver.quit()

def main():
    driver = iniciar_driver()

    try:
        iniciar_sesion(driver, "standard_user", "secret_sauce")
        agregar_producto_al_carrito(driver)
        verificar_producto_en_carrito(driver)
        eliminar_producto_del_carrito(driver)
        verificar_carrito_vacio(driver)
    except AssertionError as e:
        print(f"[Error] {e}")
    finally:
        crear_reporte()
        cerrar_driver(driver)

if __name__ == "__main__":
    main()
