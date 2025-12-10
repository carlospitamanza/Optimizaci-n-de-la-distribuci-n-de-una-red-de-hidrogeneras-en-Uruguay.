#import pandas as pd
import numpy as np
import os

def leer_excel_y_obtener_datos():
    df = pd.read_excel('Estaciones-de-servicio-utm-2.xlsx')
    mapeo_numeraciones_departamentos = df.set_index('Numeraciones')['Departamento'].to_dict()
    coordenadas_nodos = df.set_index('Numeraciones')[['ESTE', 'NORTE']].to_dict('index')
    return mapeo_numeraciones_departamentos, coordenadas_nodos

def leer_coordenadas_y_construir_mapa():
    conexiones_nodos = {}
    with open('Coordenadas-7.txt', 'r') as file:
        for line in file:
            partes = line.strip().split(': ')
            nodo = int(partes[0])
            if len(partes) > 1 and partes[1]:
                conexiones = list(map(int, partes[1].split(', ')))
            else:
                conexiones = []
            conexiones_nodos[nodo] = conexiones
    return conexiones_nodos

def calcular_distancia(coord1, coord2):
    return np.sqrt((coord1['ESTE'] - coord2['ESTE']) ** 2 + (coord1['NORTE'] - coord2['NORTE']) ** 2)

def encontrar_nodo_mas_cercano(nodo, nodos_departamento, coordenadas_nodos):
    nodo_coord = coordenadas_nodos[nodo]
    distancia_minima = float('inf')
    nodo_mas_cercano = None
    for otro_nodo in nodos_departamento:
        if otro_nodo != nodo:
            distancia = calcular_distancia(nodo_coord, coordenadas_nodos[otro_nodo])
            if distancia < distancia_minima:
                distancia_minima = distancia
                nodo_mas_cercano = otro_nodo
    return nodo_mas_cercano

def generar_archivos_por_departamento(conexiones_nodos, mapeo_numeraciones_departamentos, coordenadas_nodos):
    departamentos_unicos = set(mapeo_numeraciones_departamentos.values())
    departamentos_limpio = {depto.strip(): [] for depto in departamentos_unicos}

    for nodo, conexiones in conexiones_nodos.items():
        departamento_nodo = mapeo_numeraciones_departamentos.get(nodo, '').strip()
        if departamento_nodo:
            conexiones_filtradas = [c for c in conexiones if mapeo_numeraciones_departamentos.get(c, '').strip() == departamento_nodo]
            if not conexiones_filtradas:  # Nodo aislado
                nodos_departamento = [n for n, d in mapeo_numeraciones_departamentos.items() if d.strip() == departamento_nodo]
                nodo_mas_cercano = encontrar_nodo_mas_cercano(nodo, nodos_departamento, coordenadas_nodos)
                if nodo_mas_cercano:
                    conexiones_filtradas = [nodo_mas_cercano]
            departamentos_limpio[departamento_nodo].append((nodo, conexiones_filtradas))

    for depto, conexiones in departamentos_limpio.items():
        if conexiones:
            archivo_depto_path = f"Coordenadas_{depto}.txt"
            with open(archivo_depto_path, 'w') as archivo_depto:
                for nodo, conexiones in conexiones:
                    conexiones_str = ', '.join(map(str, conexiones))
                    archivo_depto.write(f"{nodo}: {conexiones_str}\n")

if __name__ == "__main__":
    mapeo_numeraciones_departamentos, coordenadas_nodos = leer_excel_y_obtener_datos()
    conexiones_nodos = leer_coordenadas_y_construir_mapa()  # Asume que la función ya está definida
    generar_archivos_por_departamento(conexiones_nodos, mapeo_numeraciones_departamentos, coordenadas_nodos)

    print("Archivos de coordenadas por departamento generados con éxito.")

