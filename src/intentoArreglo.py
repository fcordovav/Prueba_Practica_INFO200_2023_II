import openpyxl
import numpy as np
import matplotlib.pyplot as plt
from pulp import *

# Tomo los valores del excel, solo modificar los num en el excel 

wb = openpyxl.load_workbook("problema.xlsx")
sheet = wb.active
funcionObjetivo = [sheet["C3"].value, sheet["D3"].value, sheet["E3"].value]
restriccionesMenorIgual = [
    [sheet["C4"].value, sheet["D4"].value, sheet["E4"].value],
    [sheet["C5"].value, sheet["D5"].value, sheet["E5"].value],
    [sheet["C6"].value, sheet["D6"].value, sheet["E6"].value],
]
restriccionesMayorIgual = [
    [sheet["C7"].value, sheet["D7"].value, sheet["E7"].value],
    [sheet["C8"].value, sheet["D8"].value, sheet["E8"].value],
]

print(funcionObjetivo)
print(restriccionesMenorIgual)
print(restriccionesMayorIgual)

#####################################
#### Para obtener solución óptima ###
#####################################
# Con esto evito un mensaje enorme en consola
pulp.LpSolverDefault.msg = 0

# Definir el problema de optimización
problema = LpProblem("testeo", LpMaximize)

# Variables
x = LpVariable("x", lowBound=100)
y = LpVariable("y", 100, 700)

# Función objetivo
problema += funcionObjetivo[0] * x + funcionObjetivo[1] * y, "obj"

# Restricciones
problema += restriccionesMenorIgual[0][0] * x + restriccionesMenorIgual[0][1] * y <= restriccionesMenorIgual[0][2], "cl_1"
problema += restriccionesMenorIgual[1][0] * x + restriccionesMenorIgual[1][1] * y <= restriccionesMenorIgual[1][2], "cl_2"
problema.solve()

# Valores óptimos de x e y
x_opt = x.varValue
y_opt = y.varValue

# Valor óptimo de la función objetivo
print(f"Max Z = {value(problema.objective)}")


#########################################
#### Para graficas las restricciones ####
#########################################

### Encontrar todos los puntos de interseccion entre las rectas de las restricciones ###
puntos_interseccion = []

# Función para encontrar la intersección entre dos restricciones
def encontrar_interseccion(restriccion1, restriccion2):
    A = np.array([restriccion1[:2], restriccion2[:2]])
    b = np.array([restriccion1[2], restriccion2[2]])
    try:
        punto = np.linalg.solve(A, b)
        return punto
    except np.linalg.LinAlgError:
        return None


# Iterar a través de todas las combinaciones de restricciones, Para encontrar las intersecciones
for i, restriccion1 in enumerate(restriccionesMenorIgual + restriccionesMayorIgual):
    for j, restriccion2 in enumerate(restriccionesMenorIgual + restriccionesMayorIgual):
        if i != j:  # Evitar comparar la misma restricción
            punto = encontrar_interseccion(restriccion1, restriccion2)
            if punto is not None:
                puntos_interseccion.append(punto)

### Para ver que puntos de puntos_interseccion cumplen todas las condiciones ###
puntosPolinomio = []

# Verificar si los puntos de intersección cumplen todas las restricciones
for punto in puntos_interseccion:
    cumple_todas = True
    for restriccion in restriccionesMenorIgual:
        if punto[0] * restriccion[0] + punto[1] * restriccion[1] > restriccion[2]:
            cumple_todas = False
            break
    for restriccion in restriccionesMayorIgual:
        if punto[0] * restriccion[0] + punto[1] * restriccion[1] < restriccion[2]:
            cumple_todas = False
            break
    if cumple_todas:
        puntosPolinomio.append(punto)

### Eliminar puntos repetidos en puntosPolinomio ###
puntosPolinomio = list(set(tuple(p) for p in puntosPolinomio))

#########################
#### Graficar Rectas ####
#########################

# Definir el rango de valores de x y y para las restricciones como igualdades
X = np.linspace(0, 1000, 400)
Y = np.linspace(0, 1000, 400)
X, Y = np.meshgrid(X, Y)

# Crear la figura
plt.figure(figsize=(8, 6))

# Calcular las desigualdades para las restricciones MenorIgual
for restriccion in restriccionesMenorIgual:
    Z = restriccion[0] * X + restriccion[1] * Y - restriccion[2]
    plt.contour(X, Y, Z, levels=[0], colors="r")

# Calcular las desigualdades para las restricciones MayorIgual
for restriccion in restriccionesMayorIgual:
    Z = restriccion[0] * X + restriccion[1] * Y - restriccion[2]
    plt.contour(X, Y, Z, levels=[0], colors="b")

# Configurar los ejes y mostrar el gráfico
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Restricciones")
plt.xticks(np.arange(0, 1001, 100))
plt.yticks(np.arange(0, 1001, 100))
plt.grid(True)

# Para mostrar los puntos en la región factible
x_puntos, y_puntos = zip(*puntosPolinomio)
plt.scatter(x_puntos, y_puntos, c="green", label="Puntos", marker="o", zorder=10)
plt.scatter(
    x_opt, y_opt, marker="*", label="Punto Óptimo", s=200, color="blue", zorder=11
)

# Guardar y mostrar la figura
plt.savefig("../images/restricciones.png")
plt.show()

# Para Graficar zona factible
x = np.linspace(0, 1000, 400)
y = np.linspace(0, 1000, 400)
x, y = np.meshgrid(x, y)

# Definir las restricciones
condicion1 = restriccionesMenorIgual[0][0] * x + restriccionesMenorIgual[0][1] * y <= restriccionesMenorIgual[0][2]
condicion2 = restriccionesMenorIgual[1][0] * x + restriccionesMenorIgual[1][1] * y <= restriccionesMenorIgual[1][2]
condicion3 = restriccionesMenorIgual[2][1] * y <= 700
condicion4 = restriccionesMayorIgual[0][0] * x >= restriccionesMayorIgual[0][2]
condicion5 = restriccionesMayorIgual[1][1] * y >= restriccionesMayorIgual[1][2]

# Combinar las restricciones con AND
region_de_interes = condicion1 & condicion2 & condicion3 & condicion4 & condicion5

# Crear una máscara booleana para la región que cumple con las restricciones
region_de_interes = np.ma.masked_where(region_de_interes == False, region_de_interes)

################################
#### Graficar zona factible ####
################################

plt.figure(figsize=(8, 6))
plt.contourf(x, y, region_de_interes, cmap="viridis", alpha=0.5)
plt.xlabel("X")
plt.ylabel("Y")
plt.title(f"Region factible: Maximizar {problema.objective}")
plt.grid(True)

# Para mostrar los puntos en la región factible
x_puntos, y_puntos = zip(*puntosPolinomio)
plt.scatter(x_puntos, y_puntos, c="red", label="Puntos", marker="o")
plt.scatter(x_opt, y_opt, marker="*", label="Punto Óptimo", s=200, color="green")
plt.legend()
plt.xticks(np.arange(0, 1001, 100))
plt.yticks(np.arange(0, 1001, 100))
plt.grid(True)

plt.text(x_opt + 20, y_opt + 20, f"Punto Óptimo: ({x_opt}, {y_opt})", fontsize=12)
plt.text(x_opt + 20, y_opt + 70, f"Max Z = {value(problema.objective)}", fontsize=12)

# Guardar y mostrar la figura
plt.savefig("../images/region_factible.png")
plt.show()


###################################################################
#### Obtener la solucion optima, pero con el arreglo de puntos ####
###################################################################

# Func optima
def f(x, y):
    return funcionObjetivo[0] * x + funcionObjetivo[1] * y

# Vertices de la zona factible
print(puntosPolinomio)

# Guarda los resultados en el arreglo tras evaluarlos en la funcion
resultados = []
for punto in puntosPolinomio:
    x, y = punto
    resultado = f(x, y)
    resultados.append(resultado)

# Imprime los resultados
for i, punto in enumerate(puntosPolinomio):
    x, y = punto
    resultado = resultados[i]
    print(f"En el punto ({x}, {y}), f(x, y) = {resultado}")
