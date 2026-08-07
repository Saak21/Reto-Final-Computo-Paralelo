import math
import time
import os
import psutil
from concurrent.futures import ProcessPoolExecutor

def cargar_datos(filename="datos.txt"):
    with open(filename, "r") as f:
        return [float(line.strip()) for line in f]

# WORKER FASE 1: Estadísticas básicas
def fase1_worker(bloque):
    max_i = float('-inf')
    min_i = float('inf')
    suma_i = 0.0
    contador_i = len(bloque)

    for x in bloque:
        if x > max_i: max_i = x
        if x < min_i: min_i = x
        suma_i += x

    return max_i, min_i, suma_i, contador_i

# WORKER FASE 2: Varianza y conteo sobre promedio
def fase2_worker(args):
    bloque, promedio = args
    suma_dif_i = 0.0
    contador_mayor_i = 0

    for x in bloque:
        suma_dif_i += (x - promedio) ** 2
        if x > promedio:
            contador_mayor_i += 1

    return suma_dif_i, contador_mayor_i

def algoritmo_paralelo(num_procesos=None):
    if num_procesos is None:
        num_procesos = os.cpu_count()

    t_inicio = time.time()
    registros = cargar_datos()
    N = len(registros)

    # División en K bloques contiguos
    tamano_bloque = N // num_procesos
    bloques = [
        registros[i * tamano_bloque : (i + 1) * tamano_bloque]
        if i < num_procesos - 1
        else registros[i * tamano_bloque :]
        for i in range(num_procesos)
    ]

    # EJECUCIÓN FASE 1
    with ProcessPoolExecutor(max_workers=num_procesos) as executor:
        res_fase1 = list(executor.map(fase1_worker, bloques))

    max_global = max(r[0] for r in res_fase1)
    min_global = min(r[1] for r in res_fase1)
    suma_global = sum(r[2] for r in res_fase1)
    contador_global = sum(r[3] for r in res_fase1)
    promedio = suma_global / contador_global

    # EJECUCIÓN FASE 2
    args_fase2 = [(bloque, promedio) for bloque in bloques]
    with ProcessPoolExecutor(max_workers=num_procesos) as executor:
        res_fase2 = list(executor.map(fase2_worker, args_fase2))

    suma_dif_total = sum(r[0] for r in res_fase2)
    contador_mayor_total = sum(r[1] for r in res_fase2)

    desviacion_estandar = math.sqrt(suma_dif_total / contador_global)

    t_fin = time.time()
    tiempo_total = t_fin - t_inicio
    ram_usada = psutil.Process().memory_info().rss / (1024 * 1024)

    print(f"=== RESULTADOS PARALELO ({num_procesos} Procesos) ===")
    print(f"Máximo: {max_global:.2f}")
    print(f"Mínimo: {min_global:.2f}")
    print(f"Promedio: {promedio:.2f}")
    print(f"Desviación Estándar: {desviacion_estandar:.2f}")
    print(f"Mayores al promedio: {contador_mayor_total}")
    print(f"Tiempo de ejecución: {tiempo_total:.4f} s")
    print(f"RAM consumida: {ram_usada:.2f} MB")

if __name__ == "__main__":
    algoritmo_paralelo()
