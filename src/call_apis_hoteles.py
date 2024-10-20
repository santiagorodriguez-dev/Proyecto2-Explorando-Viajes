import sys
import os
import http.client
import json
import pandas as pd # type: ignore

def call_api(key,datos):

    dicc_datos = dict()
    try:
        adults_number = datos[0]
        checkout_date = datos[1]
        dest_id = datos[2]
        checkin_date = datos[3]

        conn = http.client.HTTPSConnection("booking-com.p.rapidapi.com")

        headers = {
            'x-rapidapi-key': key,
            'x-rapidapi-host': "booking-com.p.rapidapi.com"
        }

        url = f"/v1/hotels/search?adults_number={adults_number}&room_number=1&include_adjacency=true&units=metric&checkout_date={checkout_date}&dest_id={dest_id}&filter_by_currency=EUR&dest_type=city&checkin_date={checkin_date}&order_by=popularity&locale=es"

        conn.request("GET", url, headers=headers)

        res = conn.getresponse()
        data = res.read()

        dicc_datos = json.loads(data.decode("utf-8"))
    except:
        print(f"Error al hacer peticion api, en call_api: {datos}")
    return dicc_datos

def tratar_datos(key,datos_input):

        rows = []
        checkout_date = datos_input[1]
        checkin_date = datos_input[3]
        destination = datos_input[4]

        dicc_datos = call_api(key,datos_input)
        
        hoteles = dicc_datos['result']

        for h in hoteles:
            row = {
                'destination': destination,
                'city': h['city'],
                'checkin_date' : checkin_date,
                'checkout_date': checkout_date,
                'address': h['address'],
                'accommodation_type_name': h['accommodation_type_name'],
                'distance': h['distance'],
                'checkin': h['checkin']['from'],
                'checkout': h['checkout']['until'],
                'review_score': h['review_score'],
                'price_total': h['price_breakdown']['all_inclusive_price'],
                'price_night': h['composite_price_breakdown']['gross_amount_per_night']['value'],
                'hotel_name': h['hotel_name'],
                'class': h['class']
                }
            rows.append(row)
    
        # devolvemos dataframe
        return pd.DataFrame(rows)

def main(key,datos_input):
    df_final = pd.DataFrame()

    for d in datos_input:
        df_temp = tratar_datos(key,d)
        df_final = pd.concat([df_final, df_temp])

    df_final.reset_index(drop=True, inplace=True)

    return df_final

