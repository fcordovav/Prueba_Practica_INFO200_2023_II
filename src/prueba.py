import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def resolver_dieta(costos_alimentos, nutrientes_alimentos, requisitos_nutricionales):
    num_alimentos = len(costos_alimentos)

    A = -nutrientes_alimentos.T
    c = costos_alimentos

    # Agregar una fila de unos al final de A para representar la restricción de costos
    A = np.vstack([A, np.ones(num_alimentos)])

    requisitos_nutricionales = np.append(requisitos_nutricionales, 0)  # Agregar un 0 para representar el costo

    result = np.linalg.lstsq(A, requisitos_nutricionales, rcond=None)

    return result[0][:-1], np.dot(result[0], c)

def mostrar_dieta(solucion, valor_optimo, costos_alimentos):
    print("Resultado de la optimización:")
    for i, cantidad in enumerate(solucion):
        print(f"Alimento {i + 1}: {cantidad} unidades")

    print(f"Costo total de la dieta: ${valor_optimo}")

def generar_graficos(solucion, costos_alimentos, nutrientes_alimentos, requisitos_nutricionales):
    num_alimentos = len(costos_alimentos)

    # Crear gráfico de restricciones
    fig, ax = plt.subplots()

    for i in range(len(requisitos_nutricionales)):
        plt.plot([0, requisitos_nutricionales[i] / nutrientes_alimentos[i][1]], [requisitos_nutricionales[i] / nutrientes_alimentos[i][0], 0], label=f"Restricción {i+1}")

    plt.scatter([solucion[i] for i in range(num_alimentos)], [0] * num_alimentos, color='red', marker='o', label='Óptimo')

    plt.xlabel('Variable X')
    plt.ylabel('Variable Y')
    plt.title('Restricciones')
    plt.legend()
    
    plt.savefig('Restricciones.png')
    plt.clf()

    # Crear gráfico de la región factible
    fig2, ax2 = plt.subplots()

    x = np.linspace(0, 200, 100)
    y1 = (requisitos_nutricionales[0] - nutrientes_alimentos[0][0] * x) / nutrientes_alimentos[0][1]
    y2 = (requisitos_nutricionales[1] - nutrientes_alimentos[1][0] * x) / nutrientes_alimentos[1][1]
    y3 = (requisitos_nutricionales[2] - nutrientes_alimentos[2][0] * x) / nutrientes_alimentos[2][1]
    polygon = Polygon([(x[i], min(y1[i], y2[i], y3[i])) for i in range(len(x))], facecolor='0.9')
    ax2.add_patch(polygon)

    plt.scatter([solucion[i] for i in range(num_alimentos)], [0] * num_alimentos, color='red', marker='o', label='Óptimo')

    plt.xlabel('Variable X')
    plt.ylabel('Variable Y')
    plt.title(f'Región Factible: ${np.dot(solucion, costos_alimentos)}')
    plt.legend()
    
    plt.savefig('RegionFactible.png')

def main():
    costos_alimentos = np.array([0.25, 0.3, 0.2, 0.5])
    nutrientes_alimentos = np.array([
        [2, 1, 0, 3],
        [1, 2, 3, 1],
        [0, 2, 1, 2],
    ])
    requisitos_nutricionales = np.array([50, 60, 30])

    solucion, valor_optimo = resolver_dieta(costos_alimentos, nutrientes_alimentos, requisitos_nutricionales)

    mostrar_dieta(solucion, valor_optimo, costos_alimentos)
    generar_graficos(solucion, costos_alimentos, nutrientes_alimentos, requisitos_nutricionales)

if __name__ == "__main__":
    main()
