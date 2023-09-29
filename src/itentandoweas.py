import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import sympy as sp


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

# Iterar a través de todas las combinaciones de restricciones
for i, restriccion1 in enumerate(restriccionesMenorIgual + restriccionesMayorIgual):
    for j, restriccion2 in enumerate(restriccionesMenorIgual + restriccionesMayorIgual):
        if i != j:  # Evitar comparar la misma restricción
            punto = encontrar_interseccion(restriccion1, restriccion2)
            if punto is not None:
                puntos_interseccion.append(punto)

# # Mostrar los puntos de intersección
# if len(puntos_interseccion) > 0:
#     print("Puntos de intersección:")
#     for i, punto in enumerate(puntos_interseccion):
#         print(f"Punto {i + 1}: ({punto[0]}, {punto[1]})")
# else:
#     print("No se encontraron puntos de intersección válidos.")

### Ver que puntos cumplen todas las restricciones ###

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

# # Mostrar los puntos que cumplen todas las restricciones
# if len(puntosPolinomio) > 0:
#     print("Puntos que cumplen todas las restricciones:")
#     for i, punto in enumerate(puntosPolinomio):
#         print(f"Punto {i + 1}: ({punto[0]}, {punto[1]})")
# else:
#     print("No se encontraron puntos que cumplan todas las restricciones.")

### Eliminar puntos repetidos ###

puntosPolinomio = list(set(tuple(p) for p in puntosPolinomio))

# # Mostrar los puntos únicos que cumplen todas las restricciones
# if len(puntosPolinomio) > 0:
#     print("Puntos únicos que cumplen todas las restricciones:")
#     for i, punto in enumerate(puntosPolinomio):
#         print(f"Punto {i + 1}: ({punto[0]}, {punto[1]})")
# else:
#     print("No se encontraron puntos únicos que cumplan todas las restricciones.")

# print(puntosPolinomio)

# ### Graficar las restricciones ###

# X = np.linspace(0, 2000, 400)  # Valores de X de 0 a 2000
# Y = np.linspace(0, 2000, 400)  # Valores de Y de 0 a 2000

# # Crear una cuadrícula de valores X e Y
# X, Y = np.meshgrid(X, Y)

# # Calcular las desigualdades para las restricciones MenorIgual
# for restriccion in restriccionesMenorIgual:
#     Z = restriccion[0] * X + restriccion[1] * Y - restriccion[2]
#     plt.contour(X, Y, Z, levels=[0], colors='r')

# # Calcular las desigualdades para las restricciones MayorIgual
# for restriccion in restriccionesMayorIgual:
#     Z = restriccion[0] * X + restriccion[1] * Y - restriccion[2]
#     plt.contour(X, Y, Z, levels=[0], colors='b')

# # Configurar los ejes y mostrar el gráfico
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.xlim(0, 2000)
# plt.ylim(0, 2000)
# plt.grid(True)
# plt.show()

### Graficar zona factible ###

puntos = np.array(puntosPolinomio)

# Separar las coordenadas X e Y
x_coords = puntos[:, 0]
y_coords = puntos[:, 1]

# Crear un polígono cerrado conectando los puntos
plt.fill(x_coords, y_coords, 'b', alpha=0.3)  # 'b' es para color azul, alpha ajusta la transparencia

# Agregar puntos individuales en el gráfico
plt.scatter(x_coords, y_coords, color='red', marker='o', label='Puntos')

# Configurar ejes y mostrar el gráfico
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Área del polígono')
plt.grid(True)
plt.legend()
plt.show()