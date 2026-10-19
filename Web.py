class Web:
    def __init__(self):
        self.elementos = []

    def apilar(self, elemento):
        self.elementos.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            return None
        return self.elementos.pop()

    def esta_vacia(self):
        return len(self.elementos) == 0

    def mostrar(self):
        return self.elementos.copy()

    def limpiar(self):
        self.elementos.clear()


class Navegador:
    def __init__(self):
        self.atras = Web()
        self.adelante = Web()
        self.historial = Web()
        self.pagina_actual = None

    def visitar(self, pagina):
        if self.pagina_actual is not None:
            self.atras.apilar(self.pagina_actual)

        self.pagina_actual = pagina
        self.historial.apilar(pagina)
        self.adelante.limpiar()

        print("Visitando:", pagina)

    def retroceder(self):
        if self.atras.esta_vacia():
            print("No hay páginas anteriores.")
            return

        self.adelante.apilar(self.pagina_actual)
        self.pagina_actual = self.atras.desapilar()

        print("Regresaste a:", self.pagina_actual)

    def avanzar(self):
        if self.adelante.esta_vacia():
            print("No hay páginas siguientes.")
            return

        self.atras.apilar(self.pagina_actual)
        self.pagina_actual = self.adelante.desapilar()

        print("Avanzaste a:", self.pagina_actual)

    def mostrar_actual(self):
        if self.pagina_actual is None:
            print("No has visitado ninguna página.")
        else:
            print("Página actual:", self.pagina_actual)

    def mostrar_historial(self):
        if self.historial.esta_vacia():
            print("El historial está vacío.")
            return

        print("\n===== HISTORIAL DE NAVEGACIÓN =====")

        for numero, pagina in enumerate(
            reversed(self.historial.mostrar()), 1
        ):
            print(f"{numero}. {pagina}")


def menu():
    navegador = Navegador()

    while True:
        print("\n========= NAVEGADOR WEB =========")
        print("1. Visitar una página")
        print("2. Retroceder")
        print("3. Avanzar")
        print("4. Mostrar página actual")
        print("5. Mostrar historial")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            pagina = input("Ingresa la URL: ").strip()

            if pagina:
                navegador.visitar(pagina)
            else:
                print("La URL no puede estar vacía.")

        elif opcion == "2":
            navegador.retroceder()

        elif opcion == "3":
            navegador.avanzar()

        elif opcion == "4":
            navegador.mostrar_actual()

        elif opcion == "5":
            navegador.mostrar_historial()

        elif opcion == "0":
            print("Cerrando navegador...")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()