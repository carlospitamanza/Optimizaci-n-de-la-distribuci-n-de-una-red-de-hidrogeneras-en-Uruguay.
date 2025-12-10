import pyomo.environ as pe
import pandas as pd

# Función para leer los datos de demanda, producción y número de nodos de cada departamento
def leer_datos_departamento(departamento):
    # Leer el archivo Excel
    df = pd.read_excel('DemandaDep.xlsx')
    # Filtrar los datos del departamento específico
    datos_departamento = df[df['Departamento'] == departamento].iloc[0]
    # Obtener los valores de demanda, producción y número de nodos
    demanda_departamento = datos_departamento['Demanda']
    porcentaje_departamento = datos_departamento['Porcentaje']
    produccion_planta = datos_departamento['Prodplanta']
    nodos_departamento = datos_departamento['Nodos']
    # Calcular D_T usando los datos del departamento
    D_T = demanda_departamento - (produccion_planta * porcentaje_departamento)
    return D_T, nodos_departamento

# Función para calcular el número de hidrogeneras y almacenes según el departamento
def calcular_hidrogeneras_almacenes(departamento, D_T, N):
    # Parámetros
    C_H = 3.2  # Coste de construir una hidrogenera
    C_A = 2.5  # Coste de construir un almacen
    Q_H = 220  # Producción anual en toneladas de hidrógeno de cada hidrogenera
    Q_A = 100  # Capacidad de almacenamiento de cada almacén anual en toneladas

    # Modelo
    modelo = pe.ConcreteModel()

    # Conjunto de nodos
    modelo.N = pe.RangeSet(N)

    # Variables
    modelo.x = pe.Var(modelo.N, within=pe.Binary)  # Hidrogeneras
    modelo.y = pe.Var(modelo.N, within=pe.Binary)  # Almacenes

    # Función Objetivo
    modelo.CT = pe.Objective(expr=sum(C_H * modelo.x[i] + C_A * modelo.y[i] for i in modelo.N), sense=pe.minimize)

    # Restricciones
    modelo.demanda = pe.Constraint(expr=sum(Q_H * modelo.x[i] + Q_A * modelo.y[i] for i in modelo.N) >= D_T)
    modelo.exclusividad = pe.ConstraintList()
    for i in modelo.N:
        modelo.exclusividad.add(modelo.x[i] + modelo.y[i] <= 1)

    # Solucionador
    solver = pe.SolverFactory('/Applications/CPLEX_Studio2211/cplex/bin/x86-64_osx/cplexamp')
    resultado = solver.solve(modelo)

    # Verificar si el modelo ha sido resuelto satisfactoriamente
    if resultado.solver.status == pe.SolverStatus.ok and resultado.solver.termination_condition == pe.TerminationCondition.optimal:
        # Calcular el número de hidrogeneras y almacenes necesarios
        hidrogeneras = sum(pe.value(modelo.x[i]) for i in modelo.N)
        almacenes = sum(pe.value(modelo.y[i]) for i in modelo.N)
        # Calcular el costo total
        costo_total = pe.value(modelo.CT)
        # Retornar los resultados
        return D_T, N, hidrogeneras, almacenes, costo_total
    else:
        print(f"No se pudo encontrar una solución óptima para el departamento {departamento}.")
        return None, None, None, None, None

# Leer los nombres de los departamentos del archivo Excel
df = pd.read_excel('DemandaDep.xlsx')
departamentos = df['Departamento']

# Listas para almacenar los resultados
resultados = []

# Calcular los resultados para cada departamento
for departamento in departamentos:
    D_T, N = leer_datos_departamento(departamento)
    if D_T is not None:
        D_T, N, hidrogeneras, almacenes, costo_total = calcular_hidrogeneras_almacenes(departamento, D_T, N)
        resultados.append((departamento, N, D_T, hidrogeneras, almacenes, costo_total))

# Crear un DataFrame con los resultados
df_resultados = pd.DataFrame(resultados, columns=['Departamento', 'N', 'D_T', 'Hidrogeneras', 'Almacenes', 'Costo Total'])

# Mostrar los resultados por pantalla
print("Resultados:")
print(df_resultados)

# Guardar los resultados en un archivo Excel
df_resultados.to_excel('Resultados.xlsx', index=False)

print("Resultados guardados en Resultados.xlsx")
