
# Ordenamiento por Burbuja (Bubble Sort)

def burbuja(lista):
    n = len(lista)

    for i in range(n):
        for j in range(0, n - i - 1):

            # Comparar elementos consecutivos
            if lista[j] > lista[j + 1]:

                # Intercambiar posiciones
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

    return lista


# Programa principal
numeros = [64, 34, 25, 12, 22, 11, 90]

print("Lista original:", numeros)

resultado = burbuja(numeros)

print("Lista ordenada:", resultado)
