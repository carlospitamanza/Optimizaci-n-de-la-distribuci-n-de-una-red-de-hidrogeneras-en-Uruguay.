# Optimizacion-de-la-distribucion-de-una-red-de-hidrogeneras-en-Uruguay.
**Programa 1 — Generación del mapa de carreteras de Uruguay**

Genera el mapa de carreteras de Uruguay a partir de un archivo shapefile y representa sobre él todas las gasolineras, asignándoles un identificador único y sus coordenadas.

**Programa 2 — Generación de la matriz de adyacencia**

Lee el archivo Coordenadas.txt con las interconexiones entre gasolineras y construye una matriz de adyacencia en Excel que formaliza dichas conexiones.

**Programa 3 — Generación del grafo simulando las carreteras uruguayas**

A partir de la matriz de adyacencia y las coordenadas de los nodos, identifica posibles errores  (como conexiones de un nodo consigo mismo) y genera la representación gráfica del grafo.

**Programa 4 — Corrección de pares de nodos incompletos**

Revisa el archivo Coordenadas.txt y corrige pares de nodos en los que la conexión no es recíproca, garantizando la simetría en el grafo.

**Programa 5 — Generación de conexiones entre nodos por departamento**

Divide el archivo de conexiones general en archivos independientes según el departamento, asignando conexiones internas y evitando nodos aislados.

**Programa 6 — Matriz de adyacencia por departamento**

Genera, para cada departamento, la matriz de adyacencia correspondiente a partir de los archivos creados previamente.

**Programa 7 — Generación del grafo por departamento**

Construye y representa el grafo de cada departamento y añade conexiones mínimas cuando es necesario para asegurar la conectividad dentro de cada región.

**Programa 8 — Resolución del Modelo 1 (Optimización del número de hidrogeneras)**

Resuelve el modelo de optimización que calcula el número óptimo de hidrogeneras de producción y de almacenamiento requeridas por cada departamento.

**Programa 9 — Resolución del Modelo 2 (Heurística de localización)**

Aplica la heurística de localización para determinar qué nodos son candidatos a hidrogeneras de producción o de almacenamiento en función de criterios geoespaciales.

**Programa 10 — Hidrogeneras disponibles por departamento según parámetro U**

Determina, dentro de un departamento concreto, qué nodos cumplen con un umbral mínimo de distancia para ser válidos como hidrogeneras de producción según el parámetro U.

