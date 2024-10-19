import sys
import os
import http.client
import json
import pandas as pd # type: ignore

def call_api(key,datos):
    
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

    conn.request("GET", f"/api/v2/flights/searchFlights?originSkyId={originSkyId}&destinationSkyId={destinationSkyId}&originEntityId={originEntityId}&destinationEntityId={destinationEntityId}&date={date}&returnDate={returnDate}&adults=0&sortBy=best&currency=EUR&market=en-ES&countryCode=ES", headers=headers)

    res = conn.getresponse()
    data = res.read()
    dicc_datos = json.loads(data.decode("utf-8"))

    return dicc_datos

def tratar_datos(dicc_datos):
    itineraries = dicc_datos['data']['itineraries']

    rows = []
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

    # Crear el DataFrame
    return pd.DataFrame(rows)

def main(key,datos):
    dicc_datos = call_api(key,datos)
    return tratar_datos(dicc_datos)




