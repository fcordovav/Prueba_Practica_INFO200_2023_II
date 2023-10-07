import numpy as np
import matplotlib.pyplot as plt
from pulp import *

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
problema += x + 4 * y, "obj"

# Restricciones
problema += 20 * x + 100 * y <= 73000, "cl_1"
problema += 30 * x + 10 * y <= 15000, "cl_2"
problema.solve()

# Valores óptimos de x e y
x_opt = x.varValue
y_opt = y.varValue

# Valor óptimo de la función objetivo
print(f"Max Z = {value(problema.objective)}")

#########################################
#### Para graficas las restricciones ####
#########################################

### Formato [Cant1X, Cant2Y, LadoDerecho] ###
restriccionesMenorIgual = [
    [20, 100, 73000],
    [30, 10, 15000],
    [0, 1, 700],
]
restriccionesMayorIgual = [
    [1,0,100],
    [0,1,100]
]

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
    plt.contour(X, Y, Z, levels=[0], colors='r')

# Calcular las desigualdades para las restricciones MayorIgual
for restriccion in restriccionesMayorIgual:
    Z = restriccion[0] * X + restriccion[1] * Y - restriccion[2]
    plt.contour(X, Y, Z, levels=[0], colors='b')

# Configurar los ejes y mostrar el gráfico
plt.xlabel('X')
plt.ylabel('Y')
plt.title("Restricciones")
plt.xticks(np.arange(0, 1001, 100))
plt.yticks(np.arange(0, 1001, 100))
plt.grid(True)

# Para mostrar los puntos en la región factible
x_puntos, y_puntos = zip(*puntosPolinomio)
plt.scatter(x_puntos, y_puntos, c='green', label='Puntos', marker='o', zorder=10)
plt.scatter(x_opt, y_opt, marker="*", label="Punto Óptimo", s=200, color="blue", zorder=11)

# Guardar y mostrar la figura
plt.savefig('../images/restricciones.png')
plt.show()

# Para Graficar zona factible
x = np.linspace(0, 1000, 400)
y = np.linspace(0, 1000, 400)
x, y = np.meshgrid(x, y)

# Definir las restricciones
condicion1 = 20*x + 100*y <= 73000
condicion2 = 30*x + 10*y <= 15000
condicion3 = y <= 700
condicion4 = x >= 100
condicion5 = y >= 100

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
plt.scatter(x_puntos, y_puntos, c='red', label='Puntos', marker='o')
plt.scatter(x_opt, y_opt, marker="*", label="Punto Óptimo", s=200, color="green")
plt.legend()
plt.xticks(np.arange(0, 1001, 100))
plt.yticks(np.arange(0, 1001, 100))
plt.grid(True)

plt.text(x_opt + 20, y_opt + 20, f'Punto Óptimo: ({x_opt}, {y_opt})', fontsize=12)
plt.text(x_opt + 20, y_opt + 70, f'Max Z = {value(problema.objective)}', fontsize=12)

# Guardar y mostrar la figura
plt.savefig('../images/region_factible.png')
plt.show()
