

import pandas as pd # type: ignore

def clean_actividades(df_actividades):
    
    df_actividades.loc[:, 'titulo'] = df_actividades['titulo'].str.capitalize().str.replace('"','')
    df_actividades.loc[:, 'ciudad'] = df_actividades['ciudad'].str.capitalize()
    df_actividades['fecha_ini'] = pd.to_datetime(df_actividades['fecha_ini'])

    return df_actividades

def clean_hoteles(df_hoteles):

    df_hoteles.loc[:, 'destination'] = df_hoteles['destination'].str.capitalize()
    df_hoteles.loc[:, 'city'] = df_hoteles['city'].str.capitalize()
    df_hoteles.loc[:, 'accommodation_type_name'] = df_hoteles['accommodation_type_name'].str.capitalize()
    df_hoteles.loc[:, 'hotel_name'] = df_hoteles['hotel_name'].str.capitalize().str.replace('"','')
    df_hoteles['checkin_date'] = pd.to_datetime(df_hoteles['checkin_date'])
    df_hoteles['class'] = df_hoteles['class'].astype(int)

    return df_hoteles

def clean_vuelos(df_vuelos):

    df_vuelos.loc[:, 'origin'] = df_vuelos['origin'].str.capitalize()
    df_vuelos.loc[:, 'destination'] = df_vuelos['destination'].str.capitalize()
    df_vuelos.loc[:, 'carriers'] = df_vuelos['carriers'].str.capitalize()
    df_vuelos['departure_date'] = pd.to_datetime(df_vuelos['departure']).dt.date
    df_vuelos['departure'] = pd.to_datetime(df_vuelos['departure']).dt.time

    return df_vuelos