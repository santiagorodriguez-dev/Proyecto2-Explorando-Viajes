# Importamos las librerías que necesitamos

# Librerías de extracción de actividades
# -----------------------------------------------------------------------
from bs4 import BeautifulSoup
import requests
import sys

sys.path.append("../")
#from src import soporte as sp
# Tratamiento de actividades
# -----------------------------------------------------------------------
import pandas as pd
import numpy as np
import re
from time import sleep
import time
import multiprocessing

# Importar librerías para automatización de navegadores web con Selenium
# -----------------------------------------------------------------------
from selenium import webdriver  # Selenium es una herramienta para automatizar la interacción con navegadores web.
from webdriver_manager.chrome import ChromeDriverManager  # ChromeDriverManager gestiona la instalación del controlador de Chrome.
from selenium.webdriver.common.keys import Keys  # Keys es útil para simular eventos de teclado en Selenium.
from selenium.webdriver.support.ui import Select  # Select se utiliza para interactuar con elementos <select> en páginas web.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException # Excepciones comunes de selenium que nos podemos encontrar

def carga_datos_previo(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    sleep(5)
    driver.close()

def obtener_actividades(url):

    carga_datos_previo(url)

    actividades = {
        'titulo': [],
        'descripcion': [],
        'precio': []
    }

    print(f"call url: {url}")
    res = requests.get(url)
    print(f"respuesta url: {res.status_code}")

    if res.status_code == 200:
        list_titulos = []
        list_descripciones = []
        list_precios = []
                
        sopa = BeautifulSoup(res.content, "html.parser")
        lista_productos = sopa.findAll("div", {"class": "o-search-list__item"} )

        for i in lista_productos:
            titulo = i.find("h2").text
            descripcion = i.find("div",{"class":"comfort-card__text l-list-card__text"}).text
            precio = i.find("span",{"class":"comfort-card__price__text"}).text

            if (len(titulo) > 0):
                list_titulos.append(str(titulo).strip())
            else:
                list_titulos.append(np.nan)
            if (len(descripcion) > 0):
                list_descripciones.append(str(descripcion).replace("\xa0"," ").strip())
            else:
                list_descripciones.append(np.nan)
            if (len(precio) > 0):
                list_precios.append(str(precio).replace("¡Gratis!","0").replace("€","").replace(",",".").strip())
            else:
                list_precios.append(np.nan)

        actividades['titulo'] = list_titulos
        actividades['descripcion'] = list_descripciones
        actividades['precio'] = list_precios

    return actividades

def procesar_pagina(datos_input):

    page = datos_input[0]
    ciudad = datos_input[1][0]
    date_1 = datos_input[1][1]
    date_2 = datos_input[1][2]

    pag_start_time = time.time()

    url_format = f"https://www.civitatis.com/es/{ciudad}/?page={page}&fromDate={date_1}&toDate={date_2}"
 
    dicc_pag = obtener_actividades(url_format)
    pag_end_time = time.time()
    print(f"\n El scrapeo de la PAGINA {page} duró {pag_end_time - pag_start_time:.2f} segundos.")

    return dicc_pag

def main(input_data, num_pag):
    start_time = time.time()

    dicc_final = {"titulo": [], "descripcion": [], "precio": []}
    
    for search_values in input_data:
        args = [(i, search_values) for i in range(1, num_pag)]    
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            resultados = pool.map(procesar_pagina, args)

        for dicc_pag in resultados:
            if dicc_pag:
                for key in dicc_final.keys():
                    dicc_final[key].extend(dicc_pag[key])

    df = pd.DataFrame(dicc_final)
    print(f"Numero de registros devueltos: {df.shape[0]}")
    print(df.head())

    end_time = time.time()
    print(f"\n El scrapeo TOTAL duró {end_time - start_time:.2f} segundos.")

if __name__ == "__main__":

    input_data =[['valencia','2024-11-01','2024-11-03'],['valencia','2024-11-08','2024-11-10']]
    num_pag = 4

    main(input_data,num_pag)