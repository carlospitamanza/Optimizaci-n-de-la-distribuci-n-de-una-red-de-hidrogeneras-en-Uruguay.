import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Definir la funciÃ³n para leer las coordenadas de los nodos
def leer_coordenadas():
    coordinates_file_path = 'Estaciones-de-servicio-utm-2.xlsx'
    df_coordinates = pd.read_excel(coordinates_file_path)
    df_coordinates = df_coordinates.set_index('Numeraciones')
    node_coordinates = df_coordinates[['LONGITUD', 'LATITUD']].to_dict(orient='index')
    return node_coordinates

# Definir la funciÃ³n para calcular la distancia euclidiana entre dos puntos
def calcular_distancia(coord1, coord2):
    return np.sqrt((coord1['LONGITUD'] - coord2['LONGITUD']) ** 2 + (coord1['LATITUD'] - coord2['LATITUD']) ** 2)

# Definir la funciÃ³n para conectar componentes desconectados
def conectar_componentes(G, node_coordinates):
    componentes = list(nx.connected_components(G))
    arista_a_anadir = None  # Inicializar la variable aquÃ­
    if len(componentes) > 1:
        mayor_componente = max(componentes, key=len)
        otros_componentes = [comp for comp in componentes if comp != mayor_componente]
        distancia_minima = float('inf')
        for componente in otros_componentes:
            for nodo1 in mayor_componente:
                for nodo2 in componente:
                    distancia = calcular_distancia(node_coordinates[nodo1], node_coordinates[nodo2])
                    if distancia < distancia_minima:
                        distancia_minima = distancia
                        arista_a_anadir = (nodo1, nodo2)
        if arista_a_anadir:
            G.add_edge(*arista_a_anadir)
    return G, arista_a_anadir

# Definir la funciÃ³n para actualizar el archivo de coordenadas con la nueva arista
def actualizar_coordenadas(nombre_departamento, arista_a_anadir):
    if arista_a_anadir:
        archivo_coordenadas = f"Coordenadas_{nombre_departamento}.txt"
        with open(archivo_coordenadas, 'a') as file:
            file.write(f"{arista_a_anadir[0]}: {arista_a_anadir[1]}\n")
            file.write(f"{arista_a_anadir[1]}: {arista_a_anadir[0]}\n")

# Definir la funciÃ³n principal para procesar cada archivo de matriz de adyacencia
def procesar_matriz_adyacencia(adjacency_file_path, nombre_departamento, node_coordinates):
    df_adjacency = pd.read_excel(adjacency_file_path, index_col=0)
    df_adjacency.index = df_adjacency.index.map(int)
    df_adjacency.columns = df_adjacency.columns.map(int)
    self_connected_nodes = [node for node in df_adjacency.index if df_adjacency.at[node, node] == 1]
    if self_connected_nodes:
        print(f"Nodos con conexiÃ³n consigo mismos en {nombre_departamento}: {self_connected_nodes}")
    else:
        print(f"No hay nodos con conexiÃ³n consigo mismos en {nombre_departamento}.")
    G = nx.from_pandas_adjacency(df_adjacency)
    G, arista_a_anadir = conectar_componentes(G, node_coordinates)
    pos = {node: (node_coordinates[node]['LONGITUD'], node_coordinates[node]['LATITUD']) for node in G.nodes() if node in node_coordinates}
    plt.figure(figsize=(15, 12))
    nx.draw(G, pos, with_labels=True, node_size=50, node_color='skyblue')
    plt.title(f"Red del Departamento: {nombre_departamento}")
    plt.savefig(f'RED_{nombre_departamento}.png', dpi=300)
    plt.close()
    actualizar_coordenadas(nombre_departamento, arista_a_anadir)

# Leer las coordenadas de los nodos una vez para todos los departamentos
node_coordinates = leer_coordenadas()

# Listar y procesar archivos
archivos_matriz = [f for f in os.listdir('.') if f.startswith("matriz_adyacencia_") and f.endswith(".xlsx")]

for archivo in archivos_matriz:
    nombre_departamento = archivo.replace("matriz_adyacencia_", "").replace(".xlsx", "")
    procesar_matriz_adyacencia(archivo, nombre_departamento, node_coordinates)
