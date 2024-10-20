import sys
import os
import http.client
import json
import pandas as pd # type: ignore

def call_api(key,datos):
    """
    Realiza una solicitud HTTP a la API de Sky Scrapper para obtener información sobre vuelos.

    Args:
        key (str): Clave de la API para autenticación.
        datos (list): Lista de datos de entrada que contiene:
            - originSkyId (str): ID del origen en el sistema Sky.
            - destinationSkyId (str): ID del destino en el sistema Sky.
            - originEntityId (str): ID de la entidad de origen.
            - destinationEntityId (str): ID de la entidad de destino.
            - date (str): Fecha de salida (formato 'YYYY-MM-DD').
            - returnDate (str): Fecha de regreso (formato 'YYYY-MM-DD').

    Returns:
        dict: Un diccionario con la respuesta JSON de la API, decodificado en un objeto Python.
              En caso de error en la solicitud o al procesar la respuesta, se devuelve un diccionario vacío.
    """

    dicc_datos = dict()
    try:
        originSkyId = datos[0]
        destinationSkyId = datos[1]
        originEntityId = datos[2]
        destinationEntityId = datos[3]
        date = datos[4]
        returnDate = datos[5]

        conn = http.client.HTTPSConnection("sky-scrapper.p.rapidapi.com")

        headers = {
            'x-rapidapi-key': key,
            'x-rapidapi-host': "sky-scrapper.p.rapidapi.com"
        }

        url = f"/api/v2/flights/searchFlights?originSkyId={originSkyId}&destinationSkyId={destinationSkyId}&originEntityId={originEntityId}&destinationEntityId={destinationEntityId}&date={date}&returnDate={returnDate}&adults=0&sortBy=best&currency=EUR&market=en-ES&countryCode=ES"

        conn.request("GET", url, headers=headers)

        res = conn.getresponse()
        data = res.read()
        dicc_datos = json.loads(data.decode("utf-8"))
    except:
        print(f"Error al hacer peticion api, en call_api: {url}")
    return dicc_datos

def tratar_datos(key,dicc_datos):
    """
    Procesa los datos obtenidos de la API para construir un DataFrame con la información de los vuelos.

    Args:
        key (str): Clave de la API para autenticación.
        dicc_datos (list): Lista con los parámetros para llamar a la API, que incluye datos del vuelo.

    Returns:
        pd.DataFrame: Un DataFrame de pandas con la información de los vuelos, incluyendo columnas como:
                      id del vuelo, precio, origen, destino, duración en minutos, fechas de salida y llegada,
                      y la aerolínea que comercializa el vuelo.
                      Si ocurre un error al procesar los datos, se devuelve un DataFrame vacío.
    """

    rows = []
    try:
        dicc_datos = call_api(key,dicc_datos)
        
        itineraries = dicc_datos['data']['itineraries']

        for itinerary in itineraries:
            price_raw = itinerary['price']['raw']

            for leg in itinerary['legs']:
                row = {
                    'id': leg['id'],
                    'price': price_raw,
                    'origin': leg['origin']['name'],
                    'destination': leg['destination']['name'],
                    'duration_minutes': leg['durationInMinutes'],
                    'departure': leg['departure'],
                    'arrival': leg['arrival'],
                    'carriers': leg['carriers']['marketing'][0]['name']
                }
                rows.append(row)
    except:
        print(f"Error al recorrer datos devueltos: {dicc_datos}")

    # Crear el DataFrame
    return pd.DataFrame(rows)

def main(key,datos):
    """
    Ejecuta el flujo completo de obtención y procesamiento de datos para múltiples entradas de vuelos.

    Args:
        key (str): Clave de la API para autenticación.
        datos (list of list): Lista de listas, donde cada sublista contiene:
            - originSkyId (str): ID del origen en el sistema Sky.
            - destinationSkyId (str): ID del destino en el sistema Sky.
            - originEntityId (str): ID de la entidad de origen.
            - destinationEntityId (str): ID de la entidad de destino.
            - date (str): Fecha de salida (formato 'YYYY-MM-DD').
            - returnDate (str): Fecha de regreso (formato 'YYYY-MM-DD').

    Returns:
        pd.DataFrame: Un DataFrame combinado que contiene la información de vuelos procesada
                      para todas las entradas en `datos`. Incluye todas las columnas generadas
                      en la función `tratar_datos`.
    """
    df_final = pd.DataFrame()

    for d in datos:
        df_temp = tratar_datos(key,d)
        df_final = pd.concat([df_final, df_temp])

    df_final.reset_index(drop=True, inplace=True)

    return df_final

