

import pandas as pd # type: ignore

def clean_actividades(df_actividades):
    """
    Limpia y formatea el DataFrame de actividades.

    Realiza las siguientes operaciones:
    - Capitaliza el título y elimina comillas.
    - Capitaliza el nombre de la ciudad.
    - Convierte la columna de fecha inicial a tipo datetime.

    Args:
        df_actividades (pd.DataFrame): DataFrame que contiene información sobre actividades,
            incluyendo columnas 'titulo', 'ciudad', y 'fecha_ini'.

    Returns:
        pd.DataFrame: DataFrame limpio y formateado de actividades.
    """
    
    df_actividades.loc[:, 'titulo'] = df_actividades['titulo'].str.capitalize().str.replace('"','')
    df_actividades.loc[:, 'ciudad'] = df_actividades['ciudad'].str.capitalize()
    df_actividades['fecha_ini'] = pd.to_datetime(df_actividades['fecha_ini'])

    return df_actividades

def clean_hoteles(df_hoteles):
    """
    Limpia y formatea el DataFrame de hoteles.

    Realiza las siguientes operaciones:
    - Capitaliza el destino, ciudad, tipo de alojamiento y nombre del hotel.
    - Convierte la columna de fecha de check-in a tipo datetime.
    - Convierte la clase del hotel a tipo entero.

    Args:
        df_hoteles (pd.DataFrame): DataFrame que contiene información sobre hoteles,
            incluyendo columnas 'destination', 'city', 'accommodation_type_name', 
            'hotel_name', 'checkin_date' y 'class'.

    Returns:
        pd.DataFrame: DataFrame limpio y formateado de hoteles.
    """

    df_hoteles.loc[:, 'destination'] = df_hoteles['destination'].str.capitalize()
    df_hoteles.loc[:, 'city'] = df_hoteles['city'].str.capitalize()
    df_hoteles.loc[:, 'accommodation_type_name'] = df_hoteles['accommodation_type_name'].str.capitalize()
    df_hoteles.loc[:, 'hotel_name'] = df_hoteles['hotel_name'].str.capitalize().str.replace('"','')
    df_hoteles['checkin_date'] = pd.to_datetime(df_hoteles['checkin_date'])
    df_hoteles['class'] = df_hoteles['class'].astype(int)

    return df_hoteles

def clean_vuelos(df_vuelos):
    """
    Limpia y formatea el DataFrame de vuelos.

    Realiza las siguientes operaciones:
    - Capitaliza el origen, destino y transportistas.
    - Convierte la columna de fecha de salida a tipo datetime y extrae la fecha y la hora.

    Args:
        df_vuelos (pd.DataFrame): DataFrame que contiene información sobre vuelos,
            incluyendo columnas 'origin', 'destination', 'carriers' y 'departure'.

    Returns:
        pd.DataFrame: DataFrame limpio y formateado de vuelos.
    """
    df_vuelos.loc[:, 'origin'] = df_vuelos['origin'].str.capitalize()
    df_vuelos.loc[:, 'destination'] = df_vuelos['destination'].str.capitalize()
    df_vuelos.loc[:, 'carriers'] = df_vuelos['carriers'].str.capitalize()
    df_vuelos['departure_date'] = pd.to_datetime(df_vuelos['departure']).dt.date
    df_vuelos['departure'] = pd.to_datetime(df_vuelos['departure']).dt.time

    return df_vuelos