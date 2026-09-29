import time

def fibonacci_500_iterativo(n):
    # Lista para guardar los 500 valores
    secuencia = []
    
    a = 0
    b = 1
    
    for _ in range(n):
        secuencia.append(a)
        # Actualizamos los valores
        siguiente = a + b
        a = b
        b = siguiente
        
    return secuencia

# ==========================================
# PRUEBA DEL PROGRAMA
# ==========================================
print("Calculando 500 valores de Fibonacci...")

inicio = time.time()
resultado = fibonacci_500_iterativo(500)
fin = time.time()

# Mostrar resultados
print("\nAquí tienes los primeros y últimos valores para no saturar tu pantalla:")
print("-" * 60)

# Imprimir los primeros 10
for i in range(10):
    print(f"Posición {i+1}: {resultado[i]}")

print("...")
print("... [480 valores omitidos visualmente] ...")
print("...")

# Imprimir los últimos 10 (del 491 al 500)
for i in range(490, 500):
    print(f"Posición {i+1}: {resultado[i]}")

print("-" * 60)
print(f"-> ¡Los 500 valores se calcularon en {(fin - inicio)*1000:.4f} milisegundos!")