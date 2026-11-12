
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None


class Arbol:
    def __init__(self):
        self.raiz = None

    def insertar(self, dato):
        if self.buscar(dato):
            return False

        self.raiz = self._insertar(self.raiz, dato)
        return True

    def _insertar(self, nodo, dato):
        if nodo is None:
            return Nodo(dato)

        if dato < nodo.dato:
            nodo.izquierdo = self._insertar(
                nodo.izquierdo, dato
            )
        elif dato > nodo.dato:
            nodo.derecho = self._insertar(
                nodo.derecho, dato
            )

        return nodo

    def buscar(self, dato):
        actual = self.raiz

        while actual is not None:
            if dato == actual.dato:
                return True

            if dato < actual.dato:
                actual = actual.izquierdo
            else:
                actual = actual.derecho

        return False

    def eliminar(self, dato):
        if not self.buscar(dato):
            return False

        self.raiz = self._eliminar(self.raiz, dato)
        return True

    def _eliminar(self, nodo, dato):
        if nodo is None:
            return None

        if dato < nodo.dato:
            nodo.izquierdo = self._eliminar(
                nodo.izquierdo, dato
            )

        elif dato > nodo.dato:
            nodo.derecho = self._eliminar(
                nodo.derecho, dato
            )

        else:
            if nodo.izquierdo is None:
                return nodo.derecho

            if nodo.derecho is None:
                return nodo.izquierdo

            sucesor = self._minimo(nodo.derecho)
            nodo.dato = sucesor.dato
            nodo.derecho = self._eliminar(
                nodo.derecho, sucesor.dato
            )

        return nodo

    def _minimo(self, nodo):
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    def preorden(self):
        resultado = []

        def recorrer(nodo):
            if nodo is not None:
                resultado.append(nodo.dato)
                recorrer(nodo.izquierdo)
                recorrer(nodo.derecho)

        recorrer(self.raiz)
        return resultado

    def inorden(self):
        resultado = []

        def recorrer(nodo):
            if nodo is not None:
                recorrer(nodo.izquierdo)
                resultado.append(nodo.dato)
                recorrer(nodo.derecho)

        recorrer(self.raiz)
        return resultado

    def postorden(self):
        resultado = []

        def recorrer(nodo):
            if nodo is not None:
                recorrer(nodo.izquierdo)
                recorrer(nodo.derecho)
                resultado.append(nodo.dato)

        recorrer(self.raiz)
        return resultado

    def altura(self):
        def calcular(nodo):
            if nodo is None:
                return 0

            izquierda = calcular(nodo.izquierdo)
            derecha = calcular(nodo.derecho)

            return 1 + max(izquierda, derecha)

        return calcular(self.raiz)

    def contar_nodos(self):
        def contar(nodo):
            if nodo is None:
                return 0

            return (
                1
                + contar(nodo.izquierdo)
                + contar(nodo.derecho)
            )

        return contar(self.raiz)

    def vaciar(self):
        self.raiz = None
