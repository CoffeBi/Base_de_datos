
class MezclaEquilibrada:

    def intercalar(self, izquierda, derecha):
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

        # Cada elemento inicia como una secuencia
        secuencias = [[x] for x in datos]

        while len(secuencias) > 1:

            # Archivos de entrada
            entrada1 = secuencias[::2]
            entrada2 = secuencias[1::2]

            # Archivos de salida
            salida1 = []
            salida2 = []

            total = max(len(entrada1), len(entrada2))

            # Combinamos las secuencias
            for i in range(total):

                izquierda = (
                    entrada1[i] if i < len(entrada1) else []
                )

                derecha = (
                    entrada2[i] if i < len(entrada2) else []
                )

                combinacion = self.intercalar(
                    izquierda, derecha
                )

                # Distribución equilibrada de las salidas
                if i % 2 == 0:
                    salida1.append(combinacion)
                else:
                    salida2.append(combinacion)

            # Reunimos las secuencias respetando su orden
            nuevas_secuencias = []
            indice1 = 0
            indice2 = 0

            for i in range(total):

                if i % 2 == 0:
                    nuevas_secuencias.append(salida1[indice1])
                    indice1 += 1
                else:
                    nuevas_secuencias.append(salida2[indice2])
                    indice2 += 1

            secuencias = nuevas_secuencias

        return secuencias[0] if secuencias else []


# Ejemplo de uso
numeros = [52, 14, 39, 7, 81, 25, 3, 60]

ordenamiento = MezclaEquilibrada()
resultado = ordenamiento.ordenar(numeros)

print("Lista original:", numeros)
print("Lista ordenada:", resultado)
