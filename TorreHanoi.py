import time

def torre_hanoi(n, origen, destino, auxiliar):
    """
    Método recursivo principal para resolver la Torre de Hanoi.
    """
    if n == 1:
        return 1
    
    # Mover n-1 discos del origen al auxiliar
    movimientos = torre_hanoi(n - 1, origen, auxiliar, destino)
    
    # Mover el disco base
    movimientos += 1
    
    # Mover los n-1 discos del auxiliar al destino
    movimientos += torre_hanoi(n - 1, auxiliar, destino, origen)
    
    return movimientos

def medir_tiempo_hanoi(discos):
    """
    Método auxiliar para ejecutar el algoritmo y medir el tiempo de ejecución.
    """
    inicio = time.perf_counter()
    total_movimientos = torre_hanoi(discos, 'A', 'C', 'B')
    fin = time.perf_counter()
    tiempo_transcurrido = fin - inicio
    return total_movimientos, tiempo_transcurrido

if __name__ == "__main__":
    print("=" * 60)
    print("      PROGRAMA TORRE DE HANOI - PYTHON (MÉTODOS)")
    print("=" * 60)
    
    # Scanner / Entrada de datos por teclado del usuario
    try:
        entrada = input("Ingresa la cantidad de discos (ej. 5, 10, 30, 64): ")
        d = int(entrada)
        
        print("-" * 60)
        print(f"Calculando para {d} discos...")
        print("-" * 60)
        
        # Validación para evitar bucles infinitos en números muy grandes
        if d >= 30:
            movs = (2**d) - 1
            print(f"Discos: {d}")
            print(f"Movimientos (2^n - 1): {movs}")
            if d == 30:
                print("Tiempo Estimado: ~2 a 5 minutos (Exponencial O(2^n))")
            else:
                print("Tiempo Estimado: ~584 mil millones de años (Imposible en tiempo real)")
        else:
            movs, tiempo = medir_tiempo_hanoi(d)
            print(f"Discos: {d}")
            print(f"Movimientos (2^n - 1): {movs}")
            print(f"Tiempo Real Medido: {tiempo:.6f} segundos")
            
    except ValueError:
        print("Error: Por favor ingresa un número entero válido.")
    
    print("=" * 60)
    