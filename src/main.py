import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import sympy as sp

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

### Graficar las restricciones como igualdades ###
X = np.linspace(0, 1000, 400)  # Valores de X de 0 a 2000
Y = np.linspace(0, 1000, 400)  # Valores de Y de 0 a 2000
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
plt.xlim(0, 1000)
plt.ylim(0, 1000)
plt.grid(True)
plt.show()

#####################################
#### Para Graficar zona factible ####
#####################################

# Definir el rango de valores de x y y
x = np.linspace(0, 1000, 400)  # Rango de valores de x
y = np.linspace(0, 1000, 400)  # Rango de valores de y
# Crear una cuadrícula de puntos (x, y)
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
# Graficar la región de interés
plt.figure(figsize=(8, 6))
plt.contourf(x, y, region_de_interes, cmap="viridis", alpha=0.5)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Región que cumple con las restricciones")
plt.grid(True)
# Para mostrar los puntos en la region factible
x_puntos, y_puntos = zip(*puntosPolinomio)  # Separar las coordenadas x e y de la lista
plt.scatter(x_puntos, y_puntos, c='red', label='Puntos', marker='o')
plt.legend()
plt.grid(True)
plt.show()
