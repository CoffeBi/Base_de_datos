import random
import statistics

datos = [random.randint(150, 250) for _ in range(50)]

media = statistics.mean(datos)
mediana = statistics.median(datos)
moda = statistics.multimode(datos)
varianza = statistics.variance(datos)
desviacion = statistics.stdev(datos)

print(f"Datos: {datos}")
print(f"Media: {media:.2f}")
print(f"Mediana: {mediana}")
print(f"Moda: {moda}")
print(f"Varianza muestral: {varianza:.2f}")
print(f"Desviación estándar: {desviacion:.2f}")