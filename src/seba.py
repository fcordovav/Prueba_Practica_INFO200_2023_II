# aqui estuve probando cosas y funcionaban bacan
from pulp import *
import matplotlib.pyplot as plt
import numpy as np


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

# Definir el rango de valores de x y y
x_values = np.linspace(0, 1000, 1000)  # Rango de valores de x
yn = np.linspace(0, 1000, 1000)  # Rango de valores de y

# Crear una cuadrícula de puntos (x, y)
xn, yn = np.meshgrid(x_values, yn)

# Definir las restricciones
condicion1 = 20 * xn + 100 * yn <= 73000
condicion2 = 30 * xn + 10 * yn <= 15000
condicion3 = yn <= 700
condicion4 = xn >= 100
condicion5 = yn >= 100

# Combinar las restricciones con AND
region_de_interes = condicion1 & condicion2 & condicion3 & condicion4 & condicion5

# Crear una máscara booleana para la región que cumple con las restricciones
region_de_interes = np.ma.masked_where(region_de_interes == False, region_de_interes)


# Gráfica de la región factible
plt.figure(figsize=(8, 6))
plt.contourf(xn, yn, region_de_interes, cmap="viridis", alpha=0.5)
plt.xlim(0, 1000)
plt.ylim(0, 800)
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.title("Región Factible ")
plt.scatter(x_opt, y_opt, color='red', marker='*', s=100, label="Solución Óptima")
plt.legend()
plt.grid(True)
plt.show()


# Valores de y para las restricciones
y1_values = (73000 - 20 * x_values) / 100  # de la restricción 1
y2_values = (15000 - 30 * x_values) / 10  # de la restricción 2

# Gráfica de las restricciones
plt.figure(figsize=(8, 6))
plt.plot(x_values, y1_values, label="20x + 100y = 73000")
plt.plot(x_values, y2_values, label="30x + 10y = 15000")
plt.axhline(y=700, color='red', label="y = 700")
plt.axhline(y=100, color='green', label="y = 100")
plt.axvline(x=100, color='blue', label="x = 100")
plt.xlim(0, 1000)
plt.ylim(0, 800)
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.title("Restricciones")
plt.scatter(x_opt, y_opt, color='red', marker='*', s=100, label="Solución Óptima")
plt.legend()
plt.grid(True)
plt.show()






