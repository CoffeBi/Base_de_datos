class Cola:
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        return None

    def ver_frente(self):
        if not self.esta_vacia():
            return self.items[0]
        return None

    def mostrar(self):
        return list(self.items)


def sumar_colas(cola_a, cola_b):
    
    cola_resultado = Cola()

    while not cola_a.esta_vacia() and not cola_b.esta_vacia():
        val_a = cola_a.desencolar()
        val_b = cola_b.desencolar()
        cola_resultado.encolar(val_a + val_b)

    return cola_resultado


def leer_cola(nombre):
   
    cola = Cola()
    entrada = input(f"Ingresa los números para la {nombre} (separados por espacio): ")
    
    # Convierte cada elemento a entero y lo encola
    for valor in entrada.strip().split():
        cola.encolar(int(valor))
        
    return cola

if __name__ == "__main__":
    print("=== LECTURA DE COLAS ===")
    cola_a = leer_cola("Cola A")
    cola_b = leer_cola("Cola B")

    print("\nCola A ingresada:", cola_a.mostrar())
    print("Cola B ingresada:", cola_b.mostrar())

    resultado = sumar_colas(cola_a, cola_b)

    print("\nCola Resultado (Suma elemento a elemento):")
    print(resultado.mostrar())