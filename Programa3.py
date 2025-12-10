#
# IDENTIFICAR SI ALGÚN NODO TIENE CONEXIÓN CONSIGO MISMO:

import pandas as pd

# Ruta al archivo de matriz de adyacencia
adjacency_file_path = 'matriz_adyacencia.xlsx'

# Cargar la matriz de adyacencia desde el archivo Excel
df_adjacency = pd.read_excel(adjacency_file_path, index_col=0)

# Obtener los nombres de los nodos (fila 1 y columna 1)
node_names = df_adjacency.index.tolist()

# Identificar nodos con conexión consigo mismos
self_connected_nodes = []

for node in node_names:
    if df_adjacency.loc[node, node] == 1:
        self_connected_nodes.append(node)

# Imprimir los nodos con conexión consigo mismos
if self_connected_nodes:
    print("Nodos con conexión consigo mismos:", self_connected_nodes)
else:
    print("No hay nodos con conexión consigo mismos.")

# REPRESENTAR LA RED:

import networkx as nx
import matplotlib.pyplot as plt

# Leer el archivo Excel con la matriz de adyacencia
adjacency_file_path = 'matriz_adyacencia.xlsx'
df_adjacency = pd.read_excel(adjacency_file_path, index_col=0)

# Obtener la matriz de adyacencia como una lista de listas
adjacency_matrix = df_adjacency.values.tolist()

# Leer el archivo Excel con las coordenadas de los nodos
coordinates_file_path = 'Estaciones-de-servicio-utm.xlsx'
df_coordinates = pd.read_excel(coordinates_file_path)

# Restablecer el índice para asegurarse de que sea único
df_coordinates = df_coordinates.set_index('Numeraciones')

# Obtener las coordenadas como un diccionario
node_coordinates = df_coordinates[['LONGITUD', 'LATITUD']].to_dict(orient='index')

# Convertir la matriz de adyacencia en una lista de tuplas de bordes
edges = []
for i in range(len(adjacency_matrix)):
    for j in range(len(adjacency_matrix[i])):
        if adjacency_matrix[i][j] == 1:
            edges.append((i + 1, j + 1))  # No convertir a cadenas

# Crear un grafo dirigido desde la lista de bordes
G = nx.Graph(edges)

# Convertir las claves del grafo a enteros
G = nx.relabel_nodes(G, lambda x: int(x))

# Crear un diccionario de posiciones directamente
pos = {node: (node_coordinates[node]['LONGITUD'], node_coordinates[node]['LATITUD']) for node in G.nodes}

# Aumentar el tamaño de la figura
fig, ax = plt.subplots(figsize=(15, 12))

# Dibujar la red
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1, node_color='skyblue', font_size=1, arrowsize=10, ax=ax)

# Ajustar el diseño para evitar cortes en la figura
plt.tight_layout()

# Guardar la figura
plt.savefig('RED.png', dpi=1000)

# Mostrar el gráfico
plt.show()
