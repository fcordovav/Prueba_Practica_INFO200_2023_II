# Prueba Práctica INFO200

## Programa

Se desarrollaron dos programas para maximizar problemas de programación lineal. El programa 'main.py' no toma inputs directamente para su ejecución, ya que resuelve el problema original. El programa 'mainConExcel.py' toma los inputs del archivo Excel llamado 'problema.xlsx', el cual se encuentra en la carpeta 'Excel'. En este archivo Excel, solo debes modificar las celdas de los valores (el formato está explicado en el mismo archivo). Ambos códigos funcionan de la misma manera, y las instrucciones se resumen de la siguiente manera:  
    1. Crear arreglos con las restricciones.
    2. Buscar los puntos de intersección entre estas restricciones, considerándolas como igualdades.
    3. Verificar qué puntos cumplen con todas las restricciones (estos serán los vértices de la zona factible).
    4. Eliminar los puntos repetidos, ya que al buscar los puntos, algunos pueden repetirse y deben ser eliminados.
    5. Encontrar el punto que maximiza la función objetivo. Esto se hace de dos formas: utilizando la librería PuLP o evaluando los puntos en la función objetivo y guardando el valor máximo. Ambas formas se implementaron en el código.
    6. Graficar las restricciones como igualdades utilizando los arreglos.
    7. Graficar la zona factible con las restricciones y los puntos.

## Para ejecutar el código
    1. Utiliza Python 3 (ejecuta 'main.py' o 'mainConExcel.py' en la consola).
        Ej: python3 main.py
    2. Asegúrate de estar ubicado en la carpeta 'src' al ejecutar el código.
    3. Si encuentras algún problema, intenta usar simplemente 'python' en lugar de 'python3'.

    Nota: 'mainConExcel.py' requiere la librería 'openpyxl'. Puedes instalarla usando el siguiente comando en la consola:
        pip install openpyxl

