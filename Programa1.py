# Representar el mapa de carreteras, junto con los nodos de cada      
# gasolinera, y las etiquetas sobre cada nodo. Las líneas (cyan) 
# se han reducido al mínimo grosor. El tamaño de los nodos y de
 # las etiquetas (labels) también.
# Es imposible hacerlo más pequeño. Los nodos son puntos rojos  # con borde negro.

# Se usa la función to_crs de GeoPandas para cambiar la 
# proyección del GeoDataFrame del archivo .shp a una proyección 
# UTM específica (en este caso, EPSG:32721). Esto garantiza que
 # ambos conjuntos de datos estén en la misma proyección, 
# permitiendo que los puntos 
# se superpongan correctamente en la figura.


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd
import time

def draw_networkx_labels_S(
    G,
    pos,
    labels=None,
    font_size=12.0,
    font_color="k",
    font_family="sans-serif",
    font_weight="normal",
    alpha=None,
    bbox=None,
    horizontalalignment="center",
    verticalalignment="center",
    ax=None,
    clip_on=True,
):
    
    import matplotlib.pyplot as plt

    if ax is None:
        ax = plt.gca()

    if labels is None:
        labels = {n: n for n in G.nodes()}

    text_items = {}  # there is no text collection so we'll fake one
    for n, label in labels.items():
        (x, y) = pos[n]
        if not isinstance(label, str):
            label = str(label)  # this makes "1" and 1 labeled the same
        t = ax.text(
            x,
            y,
            label,
            fontsize=font_size,
            color=font_color,
            family=font_family,
            weight=font_weight,
            alpha=alpha,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            transform=ax.transData,
            bbox=bbox,
            clip_on=clip_on,
        )
        text_items[n] = t

    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    return text_items


# Leer el shapefile con GeoPandas
shp=gpd.read_file("/Users/carlos/Desktop/CARLOSTFM/gis_osm_roads_free_1.shp")

# Ajustar la proyección si es necesario
# Utiliza la proyección UTM que sea adecuada para tu región
shp = shp.to_crs(epsg=32721)  # Cambia el EPSG según tus necesidades
# Esto tiene que ver con las coordenadas UTM.

# Ajustar el tamaño de la figura
fig, ax = plt.subplots(figsize=(24, 20))

# Graficar el GeoDataFrame con tamaño de nodos especificado
shp.plot(ax=ax, linewidth=0.1, color='cyan')  # Puedes ajustar este valor según tus preferencias

# Leer el archivo Excel con coordenadas UTM
df = pd.read_excel("/Users/carlos/Desktop/CARLOS TFM/Estaciones-de-servicio-utm.xlsx")

# Ajustar el tamaño de los nodos según tu necesidad
node_size = 0.03

# Crear un grafo dirigido
G = nx.DiGraph()

start_time = time.time()

# Añadir nodos al grafo con sus atributos (numeraciones)
for _, row in df.iterrows():
    numeracion = row['Numeraciones']
    este = row['ESTE']
    norte = row['NORTE']
    G.add_node(numeracion, pos=(este, norte))

# Añadir aristas (conexiones entre nodos)
G.add_edges_from(G.edges)

# Dibujar el grafo
pos = nx.get_node_attributes(G, 'pos')
labels = {node: f'({node})' for node in G.nodes}

# from little_sizes import draw_networkx_labels

# Dibujar nodos con tamaño constante
# nx.draw(G, pos, with_labels=True, node_size=node_size, node_color="red", font_size=1, edgecolors='black', linewidths=0.05, font_color="black", font_weight="bold", arrowsize=10, ax=ax)

# nx.draw_networkx_labels(G, pos, labels={node: str(node) for node in G.nodes}, font_size=0.001, font_color="black", font_weight="bold", ax=ax)

node_labels = {node: str(node) for node in G.nodes}

# Dibujar nodos con tamaño constante
# nx.draw(G, pos, with_labels=False, node_size=node_size, node_color="red", edgecolors='black', linewidths=0.05, font_size=1, arrowsize=10, ax=ax)
nx.draw(G, pos, node_size=node_size, node_color="red", edgecolors='black', linewidths=0.05, arrowsize=10, ax=ax)

## Nodos sin labels
# nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='red', ax=ax, linewidths=0.05, edgecolors='black')
# draw_networkx_labels_S(G, pos, labels=node_labels, font_size=0.05, font_color="black", font_weight="normal", ax=ax)


# Solo labels
# nx.draw_networkx_labels(G, pos, labels=node_labels , font_size=12, font_color='k', font_weight='light', horizontalalignment='center', verticalalignment='center', ax=ax)
draw_networkx_labels_S(G, pos, labels=node_labels , font_size=0.001, font_color='k', font_weight='light', horizontalalignment='center', verticalalignment='center', ax=ax)


# Añadir etiquetas de ejes
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')

# Ajustar el diseño para evitar cortes en la figura
plt.tight_layout()

# Guardar la figura
plt.savefig('combined_plot_with_axes.png', dpi=1200, facecolor='black')

# Mostrar la figura
plt.show()

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Tiempo de ejecución: {elapsed_time} segundos")
P