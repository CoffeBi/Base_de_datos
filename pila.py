class Pila:
    def __init__(self):
        self.elementos = []

    def apilar(self, elemento):
        self.elementos.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            raise ValueError("No hay suficientes operandos")
        return self.elementos.pop()

    def esta_vacia(self):
        return len(self.elementos) == 0

    def tamaño(self):
        return len(self.elementos)


def calcular(a, b, operador):
    if operador == "+":
        return a + b
    elif operador == "-":
        return a - b
    elif operador == "*":
        return a * b
    elif operador == "/":
        if b == 0:
            raise ZeroDivisionError("No se puede dividir entre cero")
        return a / b
    else:
        raise ValueError("Operador no válido")


def evaluar_postfija(expresion):
    pila = Pila()
    operadores = ["+", "-", "*", "/"]

    for elemento in expresion.split():
        if elemento in operadores:
            b = pila.desapilar()
            a = pila.desapilar()
            resultado = calcular(a, b, elemento)
            pila.apilar(resultado)
        else:
            pila.apilar(float(elemento))

    if pila.tamaño() != 1:
        raise ValueError("Expresión incorrecta")

    return pila.desapilar()


def evaluar_prefija(expresion):
    pila = Pila()
    operadores = ["+", "-", "*", "/"]

    for elemento in reversed(expresion.split()):
        if elemento in operadores:
            a = pila.desapilar()
            b = pila.desapilar()
            resultado = calcular(a, b, elemento)
            pila.apilar(resultado)
        else:
            pila.apilar(float(elemento))

    if pila.tamaño() != 1:
        raise ValueError("Expresión incorrecta")

    return pila.desapilar()


def menu():
    while True:
        print("\n===== EVALUADOR DE EXPRESIONES =====")
        print("1. Evaluar expresión postfija")
        print("2. Evaluar expresión prefija")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "0":
            print("Programa finalizado.")
            break

        elif opcion in ["1", "2"]:
            expresion = input(
                "Ingresa la expresión separada por espacios: "
            )

            try:
                if opcion == "1":
                    resultado = evaluar_postfija(expresion)
                else:
                    resultado = evaluar_prefija(expresion)

                print("Resultado:", resultado)

            except (ValueError, ZeroDivisionError) as error:
                print("Error:", error)

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()