calificaciones = [0] * 5

for i in range(5):
    entrada = int(input(f"Captura la califiacion {i + 1}: "))
    calificaciones[i] = entrada
    
print ("Calificaciones capturadas:")
print(calificaciones)