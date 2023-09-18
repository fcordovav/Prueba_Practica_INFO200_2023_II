import numpy as np
import matplotlib.pyplot as plt

def main() -> None:
    # Genera algunos datos de ejemplo
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Crea el gráfico
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label='Función seno')
    plt.title('Gráfico de la función seno')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

    # Guarda la imagen en una carpeta aparte
    carpeta_salida = 'Prueba_Practica_INFO200/carpeta imagenes'
    nombre_archivo = 'grafico_seno.png'
    ruta_completa = f'{carpeta_salida}/{nombre_archivo}'

    # Asegúrate de que la carpeta de salida exista
    import os
    os.makedirs(carpeta_salida, exist_ok=True)

    # Guarda la imagen en formato PNG
    plt.savefig(ruta_completa, dpi=300, bbox_inches='tight')

    # Muestra el gráfico en pantalla (opcional)
    plt.show()

    print(f'La imagen se ha guardado en: {ruta_completa}')

main()