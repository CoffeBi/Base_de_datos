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

    def tamano(self):
        return len(self.items)


class SistemaSeguros:
    def __init__(self, cantidad_servicios=3):
        self.colas = {i: Cola() for i in range(1, cantidad_servicios + 1)}
        
        self.contadores = {i: 0 for i in range(1, cantidad_servicios + 1)}

    def llegada_cliente(self, servicio):
        if servicio not in self.colas:
            print(f"[Error] El servicio {servicio} no existe.")
            return

        self.contadores[servicio] += 1
        numero_atencion = f"S{servicio}-{self.contadores[servicio]:03d}"
        self.colas[servicio].encolar(numero_atencion)
        print(f"-> Cliente registrado. Su número de atención es: {numero_atencion} (Personas antes: {self.colas[servicio].tamano() - 1})")

    def atender_cliente(self, servicio):
        if servicio not in self.colas:
            print(f"[Error] El servicio {servicio} no existe.")
            return

        if self.colas[servicio].esta_vacia():
            print(f"-> No hay clientes en espera para el servicio {servicio}.")
        else:
            turno = self.colas[servicio].desencolar()
            print(f"-> Llamando al turno: {turno} en ventanilla de servicio {servicio}.")


def main():
    sistema = SistemaSeguros(cantidad_servicios=3)

    print("=" * 55)
    print("      SISTEMA DE GESTIÓN DE COLAS - SEGUROS")
    print("=" * 55)
    print("Comandos disponibles:")
    print("  C <num_servicio>  -> Llegada de cliente (Ej: C 1)")
    print("  A <num_servicio>  -> Atender cliente (Ej: A 1)")
    print("  SALIR             -> Cerrar el programa")
    print("Servicios disponibles: 1, 2, 3")
    print("=" * 55)

    while True:
        entrada = input("\nIngrese comando: ").strip().upper()

        if entrada == "SALIR":
            print("Cerrando el sistema...")
            break

        partes = entrada.split()
        if len(partes) != 2:
            print("[Formato incorrecto] Use: 'C <servicio>' o 'A <servicio>'")
            continue

        comando, servicio_str = partes

        if not servicio_str.isdigit():
            print("[Error] El servicio debe ser un número entero.")
            continue

        servicio = int(servicio_str)

        if comando == "C":
            sistema.llegada_cliente(servicio)
        elif comando == "A":
            sistema.atender_cliente(servicio)
        else:
            print("[Error] Comando no reconocido. Utilice C o A.")


if __name__ == "__main__":
    main()