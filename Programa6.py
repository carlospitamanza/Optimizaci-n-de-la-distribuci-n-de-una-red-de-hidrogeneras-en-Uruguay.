#import pandas as pd
import numpy as np
import os

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    return lineas

def construir_matriz_adyacencia(lineas):
    nodos = set()
    conexiones = {}

    for linea in lineas:
        nodo, conexiones_str = map(str.strip, linea.split(':'))
        nodos.add(nodo)
        conexiones[nodo] = [n.strip() for n in conexiones_str.split(',')] if conexiones_str else []

    nodos = sorted(nodos, key=int)
    matriz = pd.DataFrame(np.zeros((len(nodos), len(nodos))), index=nodos, columns=nodos, dtype=int)

    for nodo, conexiones_nodo in conexiones.items():
        for conexion in conexiones_nodo:
            if conexion:  # Evitar conexiones vacías
                matriz.at[nodo, conexion] = 1

    return matriz

def procesar_archivos_coordenadas(directorio):
    archivos = [f for f in os.listdir(directorio) if f.startswith("Coordenadas_") and f.endswith(".txt")]
    
    for archivo in archivos:
        nombre_departamento = archivo.replace("Coordenadas_", "").replace(".txt", "")
        lineas = leer_archivo(os.path.join(directorio, archivo))
        matriz_adyacencia = construir_matriz_adyacencia(lineas)
        matriz_adyacencia.to_excel(f"matriz_adyacencia_{nombre_departamento}.xlsx")

if __name__ == "__main__":
    directorio_actual = '.'  # Asumiendo que el script se ejecuta en el mismo directorio que los archivos de coordenadas
    procesar_archivos_coordenadas(directorio_actual)
