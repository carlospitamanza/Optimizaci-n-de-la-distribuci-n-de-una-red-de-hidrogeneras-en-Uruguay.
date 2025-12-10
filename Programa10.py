import pandas as pd
import networkx as nx
import math
import time

start_time = time.time()

# Cargar datos desde Excel
df = pd.read_excel('Soriano _gasolineras.xlsx')
df_matriz = pd.read_excel('matriz_adyacencia_Soriano.xlsx', index_col=0)

# Función para calcular la distancia euclídea
def distancia_euclidiana(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)/1000

# Calcular la distancia entre cada par de nodos
def calcular_distancias(df):
    nodos = df['Numeraciones'].tolist()
    grafo = nx.Graph()
    grafo.add_nodes_from(nodos)
    for i in range(len(nodos)):
        for j in range(len(nodos)):
            if df_matriz.iloc[i, j] == 1:
                x1, y1 = df[df['Numeraciones'] == nodos[i]][['ESTE', 'NORTE']].values[0]
                x2, y2 = df[df['Numeraciones'] == nodos[j]][['ESTE', 'NORTE']].values[0]
                distancia = distancia_euclidiana(x1, y1, x2, y2)
                grafo.add_edge(nodos[i], nodos[j], weight=distancia)
    return grafo

# Definir umbral U
U =32.1 #Puedes modificar este valor según sea necesario

# Calcular distancias y construir el grafo
grafo_hidrogeneras = calcular_distancias(df)

# Encontrar las distancias entre todos los pares de nodos
distancias = dict(nx.all_pairs_dijkstra_path_length(grafo_hidrogeneras, weight='weight'))

# Conjunto para almacenar las hidrogeneras definitivas
H = set()

# Verificar qué nodos cumplen con la condición de distancia
for nodo1 in grafo_hidrogeneras.nodes:
    valid = True
    for nodo2 in grafo_hidrogeneras.nodes:
        if nodo1 != nodo2 and distancias[nodo1][nodo2] <= U:
            valid = False
            break
    if valid:
        H.add(nodo1)

print("Hidrogeneras definitivas:", H)
print("Nunmero H",len(H))
print("Tiempo de ejecución:", time.time() - start_time, "segundos")

# =============================================================================
 # Calcular la distancia entre los nodos 94 y 95
distancia_445_447= nx.shortest_path_length(grafo_hidrogeneras, source=445, target=447, weight='weight')
print("Distancia entre los nodos 445 y 447", distancia_445_447)
# =============================================================================















