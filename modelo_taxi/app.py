# Se importa bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Se carga el archivo csv
df_precios_electricos= pd.read_csv("Precios_Autos_Electricos.csv")

# Sección principal de la aplicación
st.title("Selección de Autos Eléctricos")

# Eliminar la columna "Unnamed: 0"
df_precios_electricos = df_precios_electricos.drop(columns=['Unnamed: 0'], errors='ignore')

# Preparar los datos
X = df_precios_electricos[['FastCharge_miH', 'Efficiency_Whmi', 'RapidCharge', 'Range_Miles']]
y = df_precios_electricos['PriceDollar']

# Entrenar el modelo
modelo_rf = RandomForestRegressor(n_estimators=50, random_state=42)
modelo_rf.fit(X, y)

# Obtener el presupuesto del cliente
presupuesto_cliente = st.number_input("Ingrese su presupuesto en dólares:")

# Crear nuevos datos con el presupuesto
nuevos_datos_prediccion = pd.DataFrame({'FastCharge_miH': [0], 'Efficiency_Whmi': [0], 'RapidCharge': [1], 'Range_Miles': [0]})

# Predicciones para las características basadas en el presupuesto del cliente
predicciones = modelo_rf.predict(nuevos_datos_prediccion[['FastCharge_miH', 'Efficiency_Whmi', 'RapidCharge', 'Range_Miles']])

# Asignar las predicciones a las columnas correspondientes en el DataFrame
nuevos_datos_prediccion['FastCharge_miH'] = predicciones
nuevos_datos_prediccion['Efficiency_Whmi'] = predicciones
nuevos_datos_prediccion['RapidCharge'] = 1  # Establecer la condición de RapidCharge igual a 1
nuevos_datos_prediccion['Range_Miles'] = predicciones

# Confirmar presupuesto con un botón
if st.button("Confirmar Presupuesto"):
    # Identificar autos más eficientes dentro del presupuesto del cliente y con RapidCharge igual a 1
    autos_eficientes_presupuesto = df_precios_electricos[
        (df_precios_electricos['PriceDollar'] >= presupuesto_cliente - 5000) &
        (df_precios_electricos['PriceDollar'] <= presupuesto_cliente + 5000) &
        (df_precios_electricos['RapidCharge'] == 1)
    ]

    # Ordenar el DataFrame por Range_Miles de manera descendente
    autos_eficientes_presupuesto = autos_eficientes_presupuesto.sort_values(by='Range_Miles', ascending=False)

    # Seleccionar los primeros 5 registros
    top_5_autos = autos_eficientes_presupuesto.head(5)

    # Mostrar solo las columnas específicas en lugar de toda la tabla
    st.subheader("Top de autos más eficientes dentro del presupuesto del cliente y con carga rápida:")
    st.table(top_5_autos[['Brand', 'Model', 'Range_Miles', 'PriceDollar']])

    # Recomendación si el cliente se aleja del presupuesto
    if presupuesto_cliente < df_precios_electricos['PriceDollar'].min() - 5000 or presupuesto_cliente > df_precios_electricos['PriceDollar'].max() + 5000:
        st.warning("Te recomendamos ajustar tu presupuesto para obtener mejores opciones.")




# Se cargan los datos y se entrena el modelo
df_taxi = pd.read_csv('Taxi_ML.csv')
caracteristicas = ['PULocationID', 'Dayofweek', 'Hour']
variable_objetivo = 'Demanda'
X = df_taxi[caracteristicas]
y = df_taxi[variable_objetivo]
entrenamiento, prueba, obj_entrenamiento, obj_prueba = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestRegressor()
rf_model.fit(entrenamiento, obj_entrenamiento)

# Se crea una función que tome los parámetros de entrada y devuelva la predicción
def prediccion(Id_Zona, Dia_de_la_semana, Hora):
    # Valida los valores de los parámetros
    if Dia_de_la_semana < 1 or Dia_de_la_semana > 7:
        return {"error": "El valor de día debe estar entre 1 y 7."}
    if Hora < 0 or Hora > 23:
        return {"error": "El valor de hora debe estar entre 0 y 23."}
    if Id_Zona < 43 or Id_Zona > 263:
        return {"error": "El Id ingresado no pertenece a ninguna Zona"}
    
    # Se calcula el día de la semana a partir del día ingresado
    Dia_semana = Dia_de_la_semana % 7  

    # Se crea un DataFrame con la información de la zona
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

    # Se devuelve la predicción y las zonas probables
    return {
        "probabilidad_en_zona": round(Demanda[0], 2),
        "probabilidad_otras_zonas": Zonas_probables
    } 

# Se crea una función para obtener las zonas más probables
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

    # Se ordena por probabilidad en orden descendente
    probabilidades.sort(key=lambda x: x[1], reverse=True)

    # Se obtiene el top_n zonas más probables junto con sus probabilidades
    zonas_probables = [(zona, probabilidad) for zona, probabilidad in probabilidades[:top_n]]

    return zonas_probables

def main():

    # Se usa Streamlit para crear widgets de entrada
    st.title('Modelo de predicción de demanda de taxis amarillos en Manhattan-Queens, NY')
    Id_Zona = st.number_input('Id de la zona', min_value=43, max_value=263, value=43)
    Dia_de_la_semana = st.number_input('Día de la semana', min_value=1, max_value=7, value=1)
    Hora = st.number_input('Hora del día', min_value=0, max_value=23, value=0)
    resutaldo = {"probabilidad_en_zona": 0, "probabilidad_otras_zonas": 0} 
    # Se crea un botón que nos permita ejecutar la consulta 
    predecir = st.button("Predecir")
    
    # Al darle clic al botón, se llama a la función de predicción con los valores de los widgets de entrada
    
    if predecir:
        resultado = prediccion(Id_Zona, Dia_de_la_semana, Hora)
        if isinstance(resultado, dict):
            if 'error' in resultado:
                st.error(resultado['error'])
            else:
                st.success(f'La probabilidad de encontrar un viaje en la zona {Id_Zona} es {resultado["probabilidad_en_zona"]}')
                st.write('Las zonas más probables son:')
                st.table(pd.DataFrame(resultado['probabilidad_otras_zonas'], columns=['Zona', 'Probabilidad']))
        else:
            st.error("El resultado no es un diccionario válido.")

if __name__ == '__main__':
    main()


