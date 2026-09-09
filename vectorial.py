def mostrar_vector(datos):
    for elemento in datos:
        print(elemento)

def media(datos):
    suma = sum(datos)
    return suma / len(datos)

def main():
    pares = [2, 4, 6, 8, 10]
    impares = [1, 3, 5, 7, 9]

    mostrar_vector
def mostrar_vector(datos):
    for dato in datos:
        print(dato)


def media(datos):
    n = len(datos)
    suma = 0
    for dato in datos:
        suma += dato
    return suma / n

pares = [2, 4, 6, 8, 10]
impares = [1, 3, 5, 7, 9]

mostrar_vector(pares)
print(f"Media= {media(pares)}")

mostrar_vector(impares)
print(f"Media= {media(impares)}")