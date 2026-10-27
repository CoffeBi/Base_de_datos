

from dataclasses import dataclass, field
from typing import Optional


@dataclass(eq=False)
class Nodo:
    id: int
    dato: int
    liga: Optional['Nodo'] = field(default=None, repr=False)


class ListaEnlazada:
    def __init__(self):
        self.inicio: Optional[Nodo] = None
        self.nodos: dict[int, Nodo] = {}
        self.siguiente_id = 1

    def nuevo(self, dato: int) -> Nodo:
        nodo = Nodo(self.siguiente_id, dato)
        self.nodos[nodo.id] = nodo
        self.siguiente_id += 1
        return nodo

    def recorrido(self) -> list[Nodo]:
        resultado = []
        visitados = set()
        actual = self.inicio
        while actual is not None and actual.id not in visitados:
            resultado.append(actual)
            visitados.add(actual.id)
            actual = actual.liga
        return resultado

    def hay_ciclo(self) -> bool:
        ruta = self.recorrido()
        return bool(ruta and ruta[-1].liga is not None)

    def cantidad(self) -> int:
        return len(self.recorrido())

    def obtener_nodo(self, posicion: int) -> Nodo:
        ruta = self.recorrido()
        if not 1 <= posicion <= len(ruta):
            raise ValueError(f'Posición inválida; usa de 1 a {len(ruta)}.')
        return ruta[posicion - 1]

    def insertar_inicio(self, dato: int) -> Nodo:
        nuevo = self.nuevo(dato)
        nuevo.liga = self.inicio
        self.inicio = nuevo
        return nuevo

    def insertar_final(self, dato: int) -> Nodo:
        if self.inicio is None:
            return self.insertar_inicio(dato)
        if self.hay_ciclo():
            raise ValueError('No existe un final mientras haya un ciclo.')
        nuevo = self.nuevo(dato)
        self.recorrido()[-1].liga = nuevo
        return nuevo

    def insertar_posicion(self, dato: int, posicion: int) -> Nodo:
        ruta = self.recorrido()
        if not 1 <= posicion <= len(ruta) + 1:
            raise ValueError(f'Posición inválida; usa de 1 a {len(ruta) + 1}.')
        if posicion == 1:
            return self.insertar_inicio(dato)
        if posicion == len(ruta) + 1 and self.hay_ciclo():
            raise ValueError('No se puede insertar al final de un ciclo.')
        anterior = ruta[posicion - 2]
        nuevo = self.nuevo(dato)
        nuevo.liga = anterior.liga
        anterior.liga = nuevo
        return nuevo

    def buscar(self, dato: int) -> list[tuple[int, Nodo]]:
        return [(posicion, nodo) for posicion, nodo in enumerate(self.recorrido(), 1)
                if nodo.dato == dato]

    def eliminar_posicion(self, posicion: int) -> Nodo:
        ruta = self.recorrido()
        if not 1 <= posicion <= len(ruta):
            raise ValueError(f'Posición inválida; usa de 1 a {len(ruta)}.')
        eliminado = ruta[posicion - 1]
        sucesor = eliminado.liga
        if sucesor is eliminado:
            sucesor = None
        if self.inicio is eliminado:
            self.inicio = sucesor
        for otro in self.nodos.values():
            if otro is not eliminado and otro.liga is eliminado:
                otro.liga = None if sucesor is otro else sucesor
        del self.nodos[eliminado.id]
        eliminado.liga = None
        return eliminado

    def conectar(self, origen_id: int, destino_id: int) -> tuple[Nodo, Nodo]:
        origen = self.nodos.get(origen_id)
        destino = self.nodos.get(destino_id)
        if origen is None or destino is None:
            raise ValueError('No existe el ID de origen o destino.')
        if origen is destino:
            raise ValueError('Un nodo no puede apuntar a sí mismo con esta operación.')
        origen.liga = destino
        return origen, destino

    def desconectar(self, origen_id: int) -> Nodo:
        origen = self.nodos.get(origen_id)
        if origen is None:
            raise ValueError(f'No existe el nodo con ID {origen_id}.')
        origen.liga = None
        return origen

    def nodos_desconectados(self) -> list[Nodo]:
        accesibles = {n.id for n in self.recorrido()}
        return [n for n in self.nodos.values() if n.id not in accesibles]

    def obtener_datos(self) -> list[int]:
        return [n.dato for n in self.recorrido()]

    def limpiar(self) -> None:
        self.inicio = None
        self.nodos.clear()
        self.siguiente_id = 1
