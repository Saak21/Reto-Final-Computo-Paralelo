import random

def generar_dataset(filename="datos.txt", total_registros=5000000):
    print(f"Generando {total_registros:,} registros de temperatura...")
    with open(filename, "w") as f:
        for _ in range(total_registros):
            f.write(f"{random.uniform(-10.0, 50.0):.2f}\n")
    print("¡Archivo generado correctamente!")

if __name__ == "__main__":
    generar_dataset()
