
class Intercalacion:

    def mezclar(self, izquierda, derecha):
        resultado = []
        i = 0
        j = 0

        # Comparamos los elementos de ambas listas
        while i < len(izquierda) and j < len(derecha):

            if izquierda[i] <= derecha[j]:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        # Agregamos los elementos restantes
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])

        return resultado

    def ordenar(self, datos):

        # Si solo existe un elemento, ya está ordenado
        if len(datos) <= 1:
            return datos

        # Dividimos la lista en dos partes
        mitad = len(datos) // 2

        izquierda = self.ordenar(datos[:mitad])
        derecha = self.ordenar(datos[mitad:])

        # Intercalamos ambas partes
        return self.mezclar(izquierda, derecha)


# Ejemplo de uso
numeros = [38, 12, 45, 7, 23, 56, 2, 19]

ordenamiento = Intercalacion()
resultado = ordenamiento.ordenar(numeros)

print("Lista original:", numeros)
print("Lista ordenada:", resultado)
