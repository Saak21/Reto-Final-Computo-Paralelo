import math
import time
import psutil

def cargar_datos(filename="datos.txt"):
    with open(filename, "r") as f:
        return [float(line.strip()) for line in f]

def algoritmo_secuencial():
    t_inicio = time.time()

    registros = cargar_datos()
    N = len(registros)

    # Pasada 1: Máximo, Mínimo y Suma
    max_val = float('-inf')
    min_val = float('inf')
    suma = 0.0

    for x in registros:
        if x > max_val: max_val = x
        if x < min_val: min_val = x
        suma += x

    promedio = suma / N

    # Pasada 2: Desviación Estándar y Conteo > Promedio
    suma_dif = 0.0
    contador_mayor = 0

    for x in registros:
        suma_dif += (x - promedio) ** 2
        if x > promedio:
            contador_mayor += 1

    desviacion_estandar = math.sqrt(suma_dif / N)

    t_fin = time.time()
    tiempo_total = t_fin - t_inicio
    ram_usada = psutil.Process().memory_info().rss / (1024 * 1024)

    print("=== RESULTADOS SECUENCIAL ===")
    print(f"Máximo: {max_val:.2f}")
    print(f"Mínimo: {min_val:.2f}")
    print(f"Promedio: {promedio:.2f}")
    print(f"Desviación Estándar: {desviacion_estandar:.2f}")
    print(f"Mayores al promedio: {contador_mayor}")
    print(f"Tiempo de ejecución: {tiempo_total:.4f} s")
    print(f"RAM consumida: {ram_usada:.2f} MB")

if __name__ == "__main__":
    algoritmo_secuencial()
