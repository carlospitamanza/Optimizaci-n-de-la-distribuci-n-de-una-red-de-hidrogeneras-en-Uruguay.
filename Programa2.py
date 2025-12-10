# Leer el archivo 'coordenadas.TXT' y crear
# un Excel con la matriz de adyacencias:    
# El primer elemento de cada fila y de cada columna son #'Numeraciones':    
import pandas as pd

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    return lineas

def construir_matriz_adyacencia(lineas):
    nodos = set()
    conexiones = {}

    for linea in lineas:
        nodo, conexiones_str = map(str.strip, linea.split(':'))
        nodo = int(nodo)
        conexiones_lista = list(map(int, conexiones_str.split(',')))
        nodos.add(nodo)
        conexiones[nodo] = conexiones_lista

    nodos_ordenados = sorted(list(nodos))
    matriz_adyacencia = pd.DataFrame(0, columns=nodos_ordenados, index=nodos_ordenados)

    for nodo, conexiones_lista in conexiones.items():
        for conexion in conexiones_lista:
            matriz_adyacencia.at[nodo, conexion] = 1

    return matriz_adyacencia

def guardar_en_excel(matriz_adyacencia, nombre_excel):
    # Guardar en Excel
    matriz_adyacencia.to_excel(nombre_excel, index=True, header=True)

if __name__ == "__main__":
    nombre_archivo = "Coordenadas.txt"
    lineas = leer_archivo(nombre_archivo)
    matriz_adyacencia = construir_matriz_adyacencia(lineas)
    
    nombre_excel = "matriz_adyacencia.xlsx"
    guardar_en_excel(matriz_adyacencia, nombre_excel)

print(f"La matriz de adyacencia se ha guardado en {nombre_excel}.")
