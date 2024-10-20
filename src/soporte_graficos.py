import pandas as pd # type: ignore
import seaborn as sns # type: ignore
import matplotlib.pyplot as plt # type: ignore

def grafico_actividades(df_actividades):

    df_actividades['fecha_ini'] = pd.to_datetime(df_actividades['fecha_ini']).dt.date

    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df_actividades, x='fecha_ini', y='precio', hue='ciudad')

    plt.title('Distribución de precios de Actividades por Inicio del fin de semana')
    plt.xlabel('')
    plt.ylabel('Precio (EUR)')
    plt.show()

def grafico_hoteles(df_hoteles):
    df_hoteles['checkin_date'] = pd.to_datetime(df_hoteles['checkin_date']).dt.date

    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df_hoteles, x='checkin_date', y='price_total', hue='destination')


    plt.title('Distribución de Precios de alojamientos por Dia inicio de Fin de semana')
    plt.xlabel('')
    plt.ylabel('Precio Total (EUR)')
    plt.xticks(rotation=0)
    plt.show()

def grafico_vuelos(df_vuelos):
    df_vuelos['departure_date'] = pd.to_datetime(df_vuelos['departure_date']).dt.date

    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df_vuelos, x='departure_date', y='price', hue='destination')


    plt.title('Distribución de Precios de vuelos ida - vuelta')
    plt.xlabel('')
    plt.ylabel('Precio Total (EUR)')
    plt.xticks(rotation=0)
    plt.show()
