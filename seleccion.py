
# Ordenamiento por Selección (Selection Sort)

def seleccion(lista):
    n = len(lista)

    for i in range(n):

        # Suponer que el elemento actual es el menor
        menor = i

        # Buscar el elemento más pequeño
        for j in range(i + 1, n):
            if lista[j] < lista[menor]:
                menor = j

        # Intercambiar elementos
        lista[i], lista[menor] = lista[menor], lista[i]

    return lista


# Programa principal
numeros = [29, 10, 14, 37, 13, 5, 20]

print("Lista original:", numeros)

resultado = seleccion(numeros)

print("Lista ordenada:", resultado)
