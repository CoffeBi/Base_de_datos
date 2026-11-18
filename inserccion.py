
# Ordenamiento por Inserción (Insertion Sort)

def insercion(lista):
    for i in range(1, len(lista)):

        # Guardar el elemento actual
        actual = lista[i]
        j = i - 1

        # Buscar la posición correcta
        while j >= 0 and lista[j] > actual:
            lista[j + 1] = lista[j]
            j -= 1

        # Insertar el elemento
        lista[j + 1] = actual

    return lista


# Programa principal
numeros = [45, 12, 78, 34, 23, 9, 56]

print("Lista original:", numeros)

resultado = insercion(numeros)

print("Lista ordenada:", resultado)
