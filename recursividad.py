import time
import sys

# Si deseas aumentar el límite de recursividad de Python, puedes descomentar la siguiente línea:
# sys.setrecursionlimit(2000)

def ackermann(m, n):
    # Caso base 1
    if m == 0:
        return n + 1
    # Caso recursivo simple
    elif m > 0 and n == 0:
        return ackermann(m - 1, 1)
    # CASO DE RECURSIVIDAD ANIDADA
    # Observa cómo el segundo parámetro es otra llamada a la función ackermann()
    else:
        return ackermann(m - 1, ackermann(m, n - 1))

def main():
    print("=========================================")
    print("     EJEMPLO DE RECURSIVIDAD ANIDADA     ")
    print("         (Función de Ackermann)          ")
    print("=========================================")
    
    print("\nAdvertencia: Usa números muy pequeños (ej. m=1, 2 o 3 y n=1, 2, 3 o 4).")
    print("Valores más altos causarán un desbordamiento de memoria (RecursionError).\n")

    try:
        m = int(input("Ingresa el valor de m: "))
        n = int(input("Ingresa el valor de n: "))
    except ValueError:
        print("-> Error: Por favor, ingresa números enteros válidos.")
        return

    try:
        # Iniciamos a medir el tiempo
        inicio = time.time()
        
        # Llamada a la función
        resultado = ackermann(m, n)
        
        # Terminamos de medir el tiempo
        fin = time.time()
        
        tiempo_ms = (fin - inicio) * 1000  # Convertir a milisegundos
        
        print(f"\n-> El resultado de Ackermann({m}, {n}) es: {resultado}")
        print(f"-> Tiempo de cálculo: {tiempo_ms:.2f} milisegundos.")
        
    except RecursionError:
        print("\n-> ¡ERROR! La recursividad fue tan profunda que se superó el límite de la pila (RecursionError).")
        print("-> Intenta con valores más pequeños.")

# Punto de entrada del programa
if __name__ == "__main__":
    main()