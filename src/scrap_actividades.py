# Importamos las librerías que necesitamos

# Librerías de extracción de actividades
# -----------------------------------------------------------------------
from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore

# Tratamiento de actividades
# -----------------------------------------------------------------------
import pandas as pd # type: ignore
import numpy as np
import re
from time import sleep
import time
import multiprocessing

# Importar librerías para automatización de navegadores web con Selenium
# -----------------------------------------------------------------------
from selenium import webdriver  # type: ignore # Selenium es una herramienta para automatizar la interacción con navegadores web.
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore # ChromeDriverManager gestiona la instalación del controlador de Chrome.
from selenium.webdriver.common.keys import Keys  # type: ignore # Keys es útil para simular eventos de teclado en Selenium.
from selenium.webdriver.support.ui import Select  # type: ignore # Select se utiliza para interactuar con elementos <select> en páginas web.
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.common.exceptions import NoSuchElementException # type: ignore # Excepciones comunes de selenium que nos podemos encontrar

def carga_datos_previo(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    sleep(5)
    driver.close()

def obtener_actividades(url, datos_input):

    ciudad = datos_input[1][0]
    date_1 = datos_input[1][1]
    date_2 = datos_input[1][2]

    actividades = {
        'titulo': [],
        'descripcion': [],
        'precio': [],
        'ciudad': [],
        'fecha_ini': [],
        'fecha_fin': []
    }

    print(f"call url: {url}")
    res = requests.get(url)
    print(f"respuesta url: {res.status_code}")

    if res.status_code == 200:
        list_titulos = []
        list_descripciones = []
        list_precios = []
        list_ciudad = []
        list_date_1 = []
        list_date_2 = []
                
        sopa = BeautifulSoup(res.content, "html.parser")
        lista_productos = sopa.findAll("div", {"class": "o-search-list__item"} )

        if len(lista_productos) > 0:
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

                list_ciudad.append(ciudad)
                list_date_1.append(date_1)
                list_date_2.append(date_2)

            actividades['titulo'] = list_titulos
            actividades['descripcion'] = list_descripciones
            actividades['precio'] = list_precios
            actividades['ciudad'] = list_ciudad
            actividades['fecha_ini'] = list_date_1
            actividades['fecha_fin'] = list_date_2
 
    return actividades

def procesar_pagina(datos_input):
    page = datos_input[0]
    ciudad = datos_input[1][0]
    date_1 = datos_input[1][1]
    date_2 = datos_input[1][2]

    pag_start_time = time.time()

    url_format = f"https://www.civitatis.com/es/{ciudad}/?page={page}&fromDate={date_1}&toDate={date_2}"

    carga_datos_previo(url_format)
 
    dicc_pag = obtener_actividades(url_format, datos_input)
    pag_end_time = time.time()
    print(f"\n la pagina {page} duró {pag_end_time - pag_start_time:.2f} segundos.")

    return dicc_pag

def main(input_data, num_pag):
    start_time = time.time()

    dicc_result_total = {"titulo": [], 
                         "descripcion": [], 
                         "precio": [] ,
                         'ciudad': [],
                         'fecha_ini': [],
                         'fecha_fin': []
                         }
    
    for search_values in input_data:
        args = [(i, search_values) for i in range(1, num_pag)]    
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            resultados = pool.map(procesar_pagina, args)

        for dicc_pag in resultados:
            if dicc_pag:
                for key in dicc_result_total.keys():
                    dicc_result_total[key].extend(dicc_pag[key])

    df = pd.DataFrame(dicc_result_total)
    print(f"Numero de registros devueltos: {df.shape[0]}")
   
    end_time = time.time()
    print(f"\n el total duró {end_time - start_time:.2f} segundos.")
    
    return df

# if __name__ == "__main__":

#     input_data =[['valencia','2024-11-01','2024-11-03'],['valencia','2024-11-08','2024-11-10']]
#     num_pag = 4

#     main(input_data,num_pag)