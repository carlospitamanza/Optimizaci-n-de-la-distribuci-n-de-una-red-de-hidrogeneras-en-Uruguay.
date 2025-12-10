import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import math
import random
import time

start_time = time.time()

# Cargar datos desde Excel
df = pd.read_excel('Estaciones-de-servicio-utm-2.xlsx')
df_matriz = pd.read_excel('matriz_adyacencia.xlsx', index_col=0)

# Nodos y Coordenadas
nodos = df['Numeraciones'].tolist()
coordenadas = {df['Numeraciones'][i]: (df['ESTE'][i], df['NORTE'][i]) for i in df.index}

# Aristas
aristas = [(i, j) for i in df_matriz.index for j in df_matriz.columns if df_matriz.loc[i, j] == 1]

# Función para calcular la distancia euclídea
def distancia_euclidiana(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)/1000

# Pesos de las Aristas
aristas_y_pesos = {(i, j): distancia_euclidiana(df[df['Numeraciones'] == i]['ESTE'].values[0], 
                                              df[df['Numeraciones'] == i]['NORTE'].values[0],
                                              df[df['Numeraciones'] == j]['ESTE'].values[0], 
                                              df[df['Numeraciones'] == j]['NORTE'].values[0]) for i, j in aristas}

# Nodo W (el primer nodo en la lista de nodos)
nodo_W = nodos[0]
coordenadas_W = coordenadas[nodo_W]
# Aristas y pesos conectados a W
aristas_y_pesos_W = {arista: peso for arista, peso in aristas_y_pesos.items() if nodo_W in arista}


# Crear y dibujar el grafo
G = nx.Graph()
G.add_nodes_from(nodos)
for arista, peso in aristas_y_pesos.items():
    G.add_edge(*arista, weight=peso)

# Dibujar el grafo
pos = {nodo: coordenadas[nodo] for nodo in nodos}
colores = ['red' if nodo == nodo_W else 'blue' for nodo in nodos]
fig, ax = plt.subplots(figsize=(10, 8))
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=10, node_color='skyblue', font_size=8, arrowsize=10, ax=ax)

plt.tight_layout()
plt.show()

print("Nodos:", nodos)
print("Coordenadas:", coordenadas)
print("Aristas y pesos:", aristas_y_pesos)
print("Nodo W:", nodo_W)
print("Coordenadas de W:", coordenadas_W)
print("Aristas y pesos conectados a W:", aristas_y_pesos_W)


# Verificar nodos aislados
nodos_aislados = [nodo for nodo in G.nodes if G.degree(nodo) == 0]

# Imprimir los resultados
print("Aristas y pesos:", aristas_y_pesos)
print("Coordenadas de W:", coordenadas_W)
print("Aristas y pesos conectados a W:", aristas_y_pesos_W)
if nodos_aislados:
    print("Hay nodos aislados:", nodos_aislados)
else:
    print("No hay nodos aislados.")
    

# Número total de nodos y aristas
num_nodos = len(nodos)
num_aristas = len(aristas_y_pesos)
print('Número de nodos: ', num_nodos)
print('Número de aristas: ', num_aristas)

grafo_generado = G

# Diccionario para almacenar las distancias mínimas
d = {}

# Calcular la distancia mínima desde cada nodo hasta el nodo W
for nodo in nodos:
    if nodo != nodo_W:
        distancia_minima = nx.dijkstra_path_length(grafo_generado, source=nodo, target=nodo_W, weight='weight')
        d[(nodo, nodo_W)] = distancia_minima

# Calcular el promedio de todas las distancias mínimas
d_promedio = sum(d.values()) / len(d)

# Imprimir el diccionario de distancias y el promedio
# print("Distancias mínimas desde cada nodo hasta W:", d)
print("Promedio de distancias mínimas desde cada nodo hasta W:", d_promedio)


# Definir el umbral
u = 10

# Conjuntos para almacenar los nodos
A = set()
B = set()

# Separar los nodos en A o B según su distancia a W
for nodo, distancia in d.items():
    if distancia > u:
        A.add(nodo[0])
    else:
        B.add(nodo[0])

# Imprimir los conjuntos A y B
print("Conjunto A (distancia > u):", A)
print("Conjunto B (distancia <= u):", B)

# ----------------------- #

D_A_B = {}

# Calcula la distancia mínima entre todos los pares de nodos excepto W
for nodo1 in nodos:
    if nodo1 != nodo_W:
        for nodo2 in nodos:
            if nodo2 != nodo_W and nodo1 != nodo2:
                distancia_minima = nx.dijkstra_path_length(grafo_generado, source=nodo1, target=nodo2, weight='weight')
                D_A_B[(nodo1, nodo2)] = distancia_minima


D_A = {}

# Calcula la distancia mínima solo entre los nodos en el conjunto A
for nodo1 in A:
    for nodo2 in A:
        if nodo1 != nodo2:
            distancia_minima = nx.dijkstra_path_length(grafo_generado, source=nodo1, target=nodo2, weight='weight')
            D_A[(nodo1, nodo2)] = distancia_minima
            
            

# Calcular el promedio de todas las distancias D_A
D_A_promedio = sum(D_A.values()) / len(D_A)
print("Promedio de distancias mínimas entre nodos del conjunto A:", D_A_promedio)

U = 0.079
A_original = A.copy()  # Hacemos una copia para no modificar el conjunto A original
H = set()
R = set()

while A_original:
    N_j = random.choice(list(A_original))
    A_original.remove(N_j)
    H.add(N_j)
    distancias = {nodo: distancia for (nodo1, nodo), distancia in D_A.items() if nodo1 == N_j and nodo in A_original}
    
    for nodo, distancia in distancias.items():
        if distancia < U:
            R.add(nodo)
    
    A_original -= R  # Eliminar nodos en R del conjunto A

    if not A_original:
        print("Conjunto A está vacío.")
        break


# El mensaje "Conjunto A está vacío." se imprime cuando ya no quedan nodos en 
# el conjunto A_original para procesar. Esto significa que todos los nodos de 
# A han sido evaluados y, dependiendo de sus distancias respecto al umbral U, 
# han sido agregados a los conjuntos H o R. Por lo tanto, es normal ver algunos 
# nodos en H y R incluso cuando A_original está vacío.



# Es importante mencionar que este código podría no funcionar como se espera 
# si el conjunto A es pequeño o si las distancias entre los nodos tienden a 
# ser menores que el umbral U, ya que podría resultar en que muchos nodos sean 
# descartados rápidamente.

# Supongamos que queremos escoger aleatoriamente un número determinado de 
#LEN( elementos tanto de H como de R:
 
# ----------------------- #

# Crear el conjunto S
S = R.union(B)

# Excluir de d las distancias que involucren nodos en H
d_filtrado = {nodo_distancia: distancia for nodo_distancia, distancia in d.items() if nodo_distancia[0] not in H}

# F contenga las distancias mínimas entre cada par de nodos donde uno es de H y el otro es de S, además de las distancias de d_filtrado
# Iniciar F con las distancias filtradas de d
F = d_filtrado.copy()

# Agregar las distancias mínimas entre cada nodo de H y cada nodo de S
for nodo_H in H:
    for nodo_S in S:
        if (nodo_H, nodo_S) in D_A_B:
            F[(nodo_H, nodo_S)] = D_A_B[(nodo_H, nodo_S)]
        elif (nodo_S, nodo_H) in D_A_B:
            F[(nodo_S, nodo_H)] = D_A_B[(nodo_S, nodo_H)]
            
# Imprimir los resultados
# print("Conjunto S:", S)
# print("Distancias d filtradas:", d_filtrado)
# print("Distancias F:", F)

# Promedio de d_filtrado y de F:
d_filtrado_promedio = sum(d_filtrado.values()) / len(d_filtrado)
print(d_filtrado_promedio)
F_promedio = sum(F.values()) / len(F)
print(F_promedio)


z = 400
a = {}
T = set()

# Almacenar en 'a' aquellos caminos de 'F' cuyas distancias sean menores que 'z'
for camino, distancia in F.items():
    if distancia < z:
        a[camino] = distancia

# Añadir los nodos apropiados al conjunto T
for nodo1, nodo2 in a.keys():
    if nodo1 not in H and nodo1 != nodo_W:
        T.add(nodo1)
    if nodo2 not in H and nodo2 != nodo_W:
        T.add(nodo2)

# Imprimir los resultados
# print("Caminos en 'a':", a)
print("Conjunto T:", T)

import pandas as pd

# Crear DataFrames para los conjuntos H y T
df_h = pd.DataFrame(list(H), columns=['Numeraciones'])
df_t = pd.DataFrame(list(T), columns=['NumeracionesA'])

# Guardar ambos DataFrames en la misma hoja, en columnas consecutivas, en el mismo archivo Excel
with pd.ExcelWriter('candidatos.xlsx', engine='xlsxwriter') as writer:
    df_h.to_excel(writer, index=False, startcol=0, startrow=0)  # Guardar H en la primera columna
    df_t.to_excel(writer, index=False, startcol=1, startrow=0)  # Guardar T en la segunda columna

print("Conjunto H guardado en 'candidatos.xlsx' bajo la columna 'Numeraciones'.")
print("Conjunto T guardado en 'candidatos.xlsx' bajo la columna 'NumeracionesA'.")

