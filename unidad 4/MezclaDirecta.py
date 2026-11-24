
class MezclaDirecta:

    def mezclar(self, izquierda, derecha):
        resultado = []
        i = 0
        j = 0

        while i < len(izquierda) and j < len(derecha):

            if izquierda[i] <= derecha[j]:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])

        return resultado

    def ordenar(self, datos):

        resultado = datos.copy()
        n = len(resultado)

        # Tamaño inicial de las secuencias
        tamaño = 1

        while tamaño < n:

            temporal = []

            # Combinamos bloques de dos en dos
            for i in range(0, n, tamaño * 2):

                izquierda = resultado[i:i + tamaño]
                derecha = resultado[i + tamaño:i + tamaño * 2]

                combinacion = self.mezclar(
                    izquierda, derecha
                )

                temporal.extend(combinacion)

            resultado = temporal
            tamaño *= 2

        return resultado


# Ejemplo de uso
numeros = [34, 8, 21, 5, 67, 12, 3, 45]

ordenamiento = MezclaDirecta()
resultado = ordenamiento.ordenar(numeros)

print("Lista original:", numeros)
print("Lista ordenada:", resultado)
