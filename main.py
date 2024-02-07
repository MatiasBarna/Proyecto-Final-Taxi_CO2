from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from fastapi import FastAPI, Query

app = FastAPI()

#Inicio
@app.get('/')
def start():
    return {'Mensaje': 'Proyecto final - Modelo de predicción'}

df_taxi = pd.read_csv('Taxi_ML.csv')

# Se seleccionan las características (X) y la variable objetivo (Y)
caracteristicas = ['PULocationID', 'Dayofweek', 'Hour']
variable_objetivo = 'Demanda'

X = df_taxi[caracteristicas]
y = df_taxi[variable_objetivo]

# Se dividen los datos en características (X) y etiquetas (y) en conjuntos de entrenamiento (X_entrenamiento, y_entrenamiento) y prueba (X_prueba, y_prueba)
entrenamiento, prueba, obj_entrenamiento, obj_prueba = train_test_split(X, y, test_size=0.2, random_state=42)

#Se crea una instancia del modelo RandomForestRegressor
rf_model = RandomForestRegressor()
rf_model.fit(entrenamiento, obj_entrenamiento)

#Se utilizan las características del conjunto de prueba (Entrenamiento) para hacer predicciones
predictiones = rf_model.predict(prueba)


# Se define la ruta y los parámetros de la API con descripciones
@app.get("/Demanda zonas")
def prediccion(
    Id_Zona: int = Query(..., Title="Id de la zona", Description="Id de la zona de localización (entre 43 y 263)."),
    Dia_de_la_semana: int = Query(..., Title="Día de la Semana", Description="Día de la semana (entre 1 y 7)."),
    Hora: int = Query(..., Title="Hora", Description="Hora del día (entre 0 y 23)."),
):
    # Se valida que los valores de día, hora e Id estén dentro del rango deseado
    if Dia_de_la_semana < 1 or Dia_de_la_semana > 7:
        return {"error": "El valor de día debe estar entre 1 y 7."}
    if Hora < 0 or Hora > 23:
        return {"error": "El valor de hora debe estar entre 0 y 23."}
    if Id_Zona < 43 or Id_Zona > 263:
        return {"error": "El Id ingresado no pertenece a ninguna Zona"}
    
    # Se calcula el día de la semana a partir del día ingresado
    Dia_semana = Dia_de_la_semana % 7  

    Zona = {
        'PULocationID': [Id_Zona],
        'Dayofweek': [Dia_semana],
        'Hour': [Hora],
    }
    loc = pd.DataFrame(Zona)

    # Se realiza la predicción de probabilidad de encontrar un viaje en la zona actual
    Demanda = rf_model.predict(loc)

    # Se obtienen las 5 zonas más probables
    Zonas_probables = zonas_mas_probables(rf_model, Id_Zona, Hora, Dia_semana, 5)
 

    return {
        "probabilidad_en_zona": round(Demanda[0], 2),
        "probabilidad_otras_zonas": Zonas_probables
    } 

# Función para obtener las zonas más probables
def zonas_mas_probables(rf_model, zona_actual, hora, dia_semana, top_n):
    zonas = list(range(43, 263)) 
    zonas.remove(zona_actual)  
    probabilidades = []

    for zona in zonas:
        localizacion_zona = {
            'PULocationID': [zona],
            'Dayofweek': [dia_semana],
            'Hour': [hora],
        }
    
        # Se crea un DataFrame con la información de la localización
        loc_zone = pd.DataFrame(localizacion_zona)
        probabilidad = rf_model.predict(loc_zone)
        probabilidades.append((zona, probabilidad[0]))

    # Ordenamos por probabilidad en orden descendente
    probabilidades.sort(key=lambda x: x[1], reverse=True)

    # Se obtiene el top_n zonas más probables junto con sus probabilidades
    zonas_probables = [(zona, probabilidad) for zona, probabilidad in probabilidades[:top_n]]

    return zonas_probables
