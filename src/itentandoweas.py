import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import sympy as sp


# Formato [Cant1X, Cant2Y, LadoDerecho]
restriccionesMenorIgual = [
    [20, 100, 73000],
    [30, 10, 15000],
    [0, 1, 700],
]

restriccionesMayorIgual = [
    [1,0,100],
    [0,1,100]
]

# Encontrar todos los puntos de interseccion entre las rectas de las restricciones

# Ver que puntos cumplen todas las restricciones

# Los puntos restantes deberian de ser los que forman el polinomio de la zona factible



X = np.linspace(0, 2000, 400)  # Valores de X de 0 a 2000
Y = np.linspace(0, 2000, 400)  # Valores de Y de 0 a 2000

# Crear una cuadrícula de valores X e Y
X, Y = np.meshgrid(X, Y)

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
plt.xlim(0, 2000)
plt.ylim(0, 2000)
plt.grid(True)
plt.show()