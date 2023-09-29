import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import sympy as sp
restricciones = [
    [6, 12, 396],
    [12, 30, 816],
    [4, 12, 312],
    [20, 30, 1200]
]

# Crear un rango de valores para x
x = np.linspace(0, 100, 100)

# Crear un gráfico
plt.figure(figsize=(8, 6))

# Crear el área factible sombreada
for i, restriccion in enumerate(restricciones):
    a, b, c = restriccion
    y = (c - a * x) / b
    if i == 0:
        plt.fill_between(x, 0, y, where=(y >= 0), alpha=0.5, label='Área Factible')
    else:
        plt.fill_between(x, 0, y, where=(y >= 0), alpha=0.5)

# Establecer límites en los ejes
plt.xlim(0, None)
plt.ylim(0, None)

# Etiquetas y título
plt.xlabel('Eje X')
plt.ylabel('Eje Y')
plt.title('Área Factible')

# Agregar leyenda
plt.legend()

# Mostrar el gráfico sin las líneas de las restricciones
plt.grid(False)
plt.show()