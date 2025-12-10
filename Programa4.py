# CORREGIR PARES DE NODOS INCOMPLETOS:

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    return lineas

def corregir_conexiones(lineas):
    grafo = {}
    for linea in lineas:
        if ":" in linea:
            nodo, conexiones_str = map(str.strip, linea.split(':'))
            nodo = int(nodo)
            conexiones = [int(x) for x in conexiones_str.split(',') if x.strip()]
            grafo[nodo] = conexiones

    for nodo, conexiones in grafo.items():
        for conexion in conexiones:
            if nodo not in grafo[conexion]:
                grafo[conexion].append(nodo)

    lineas_corregidas = [f"{nodo}: {', '.join(map(str, conexiones))}\n" for nodo, conexiones in grafo.items()]
    return lineas_corregidas

def escribir_archivo(nombre_archivo, lineas_corregidas):
    with open(nombre_archivo, 'w') as archivo:
        archivo.writelines(lineas_corregidas)
        
if __name__ == "__main__":
    nombre_archivo = "Coordenadas.txt"
    lineas = leer_archivo(nombre_archivo)
    lineas_corregidas = corregir_conexiones(lineas)
    escribir_archivo(nombre_archivo, lineas_corregidas)

print("Corrección completada.")
