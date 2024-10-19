import sys
import os
import http.client
import json
import pandas as pd # type: ignore

def call_api(key,datos):

    dicc_datos = dict()
    try:
        originSkyId = datos[0]
        destinationSkyId = datos[1]
        originEntityId = datos[2]
        destinationEntityId = datos[3]
        date = datos[4]
        returnDate = datos[5]

        conn = http.client.HTTPSConnection("booking-com.p.rapidapi.com")

        headers = {
            'x-rapidapi-key': key,
            'x-rapidapi-host': "booking-com.p.rapidapi.com"
        }

        conn.request("GET", "/v1/hotels/search?adults_number=2&room_number=1&include_adjacency=true&units=metric&checkout_date=2024-11-03&dest_id=-406132&filter_by_currency=EUR&dest_type=city&checkin_date=2024-11-01&order_by=popularity&locale=es", headers=headers)

        res = conn.getresponse()
        data = res.read()

        dicc_datos = json.loads(data.decode("utf-8"))
    except:
        print(f"Error al hacer peticion api, en call_api: {datos}")
    return dicc_datos

def tratar_datos(key,dicc_datos):

        rows = []
    
        dicc_datos = call_api(key,dicc_datos)
        
        hoteles = dicc_datos['result']

        for h in hoteles:
            row = {
                'district': h['district'],
                'city': h['city'],
                'accommodation_type_name': h['accommodation_type_name'],
                'distance': h['distance'],
                'checkin': h['checkin']['from'],
                'checkout': h['checkout']['until'],
                'review_score': h['review_score'],
                'address': h['address'],
                'price_total': h['price_breakdown']['all_inclusive_price'],
                'price_night': h['composite_price_breakdown']['gross_amount_per_night']['value'],
                'hotel_name': h['hotel_name'],
                'class': h['class'],
                }
            rows.append(row)
    

            # Crear el DataFrame
        return pd.DataFrame(rows)

def main(key,datos):
    df_final = pd.DataFrame()

    for d in datos:
        df_temp = tratar_datos(key,d)
        df_final = pd.concat([df_final, df_temp])

    df_final.reset_index(drop=True, inplace=True)

    return df_final

