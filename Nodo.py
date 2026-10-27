
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ==========================================
# PALETA MORADA
# ==========================================

FONDO = "#100D1C"
PANEL = "#1C1630"
PANEL_CLARO = "#29203F"
MORADO = "#7C3AED"
MORADO_OSCURO = "#5B21B6"
LILA = "#C4B5FD"
LILA_CLARO = "#EDE9FE"
LILA_SELECCION = "#DDD6FE"
TEXTO = "#F5F3FF"
TEXTO_SECUNDARIO = "#C4B5FD"
ROJO = "#BE185D"


# ==========================================
# CLASE NODO
# ==========================================

class Nodo:
    def __init__(self, identificador, dato):
        self.id = identificador
        self.dato = dato
        self.liga = None


# ==========================================
# CLASE LISTA ENLAZADA
# ==========================================

class ListaEnlazada:
    def __init__(self):
        self.inicio = None
        self.nodos = {}
        self.siguiente_id = 1

    def nuevo(self, dato):
        nodo = Nodo(self.siguiente_id, dato)
        self.nodos[nodo.id] = nodo
        self.siguiente_id += 1
        return nodo

    def recorrido(self):
        resultado = []
        actual = self.inicio
        vistos = set()

        while actual is not None and actual.id not in vistos:
            vistos.add(actual.id)
            resultado.append(actual)
            actual = actual.liga

        return resultado

    def hay_ciclo(self):
        camino = self.recorrido()
        return bool(
            camino and camino[-1].liga is not None
        )

    def cantidad(self):
        return len(self.recorrido())

    # INSERTAR AL INICIO
    def insertar_inicio(self, dato):
        nuevo = self.nuevo(dato)
        nuevo.liga = self.inicio
        self.inicio = nuevo
        return nuevo

    # INSERTAR AL FINAL
    def insertar_final(self, dato):
        if self.inicio is None:
            return self.insertar_inicio(dato)

        if self.hay_ciclo():
            raise ValueError(
                "La lista tiene un ciclo. "
                "No existe un final; modifica la conexión "
                "antes de insertar al final."
            )

        nuevo = self.nuevo(dato)
        self.recorrido()[-1].liga = nuevo
        return nuevo

    # INSERTAR EN UNA POSICIÓN
    def insertar_posicion(self, dato, posicion):
        ruta = self.recorrido()

        if not 1 <= posicion <= len(ruta) + 1:
            raise ValueError(
                f"Posiciones válidas para insertar: "
                f"1 a {len(ruta) + 1}."
            )

        if posicion == 1:
            return self.insertar_inicio(dato)

        if posicion == len(ruta) + 1 and self.hay_ciclo():
            raise ValueError(
                "No se puede insertar al final "
                "de una lista con ciclo."
            )

        previo = ruta[posicion - 2]
        nuevo = self.nuevo(dato)

        nuevo.liga = previo.liga
        previo.liga = nuevo

        return nuevo

    # BUSCAR DATO
    def buscar(self, dato):
        return [
            (i, n)
            for i, n in enumerate(self.recorrido(), 1)
            if n.dato == dato
        ]

    # ELIMINAR POR POSICIÓN
    def eliminar_posicion(self, posicion):
        ruta = self.recorrido()

        if not 1 <= posicion <= len(ruta):
            raise ValueError(
                f"Posiciones válidas para eliminar: "
                f"1 a {len(ruta)}."
            )

        nodo = ruta[posicion - 1]
        sucesor = nodo.liga

        if sucesor is nodo:
            sucesor = None

        if self.inicio is nodo:
            self.inicio = sucesor

        # Actualizar todas las referencias entrantes
        for otro in self.nodos.values():
            if otro is not nodo and otro.liga is nodo:
                otro.liga = (
                    None if sucesor is otro else sucesor
                )

        del self.nodos[nodo.id]
        nodo.liga = None

        return nodo

    # CONECTAR DOS NODOS
    def conectar(self, origen_id, destino_id):
        origen = self.nodos.get(origen_id)
        destino = self.nodos.get(destino_id)

        if origen is None:
            raise ValueError(
                f"No existe el nodo de origen "
                f"con ID {origen_id}."
            )

        if destino is None:
            raise ValueError(
                f"No existe el nodo de destino "
                f"con ID {destino_id}."
            )

        if origen is destino:
            raise ValueError(
                "No se permite que un nodo "
                "apunte a sí mismo."
            )

        # Reemplaza la conexión anterior
        origen.liga = destino

        return origen, destino

    # DESCONECTAR NODO
    def desconectar(self, origen_id):
        origen = self.nodos.get(origen_id)

        if origen is None:
            raise ValueError(
                f"No existe el nodo con ID {origen_id}."
            )

        origen.liga = None
        return origen

    # LIMPIAR LISTA
    def limpiar(self):
        self.inicio = None
        self.nodos.clear()
        self.siguiente_id = 1


# ==========================================
# INTERFAZ GRÁFICA
# ==========================================

class Aplicacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.lista = ListaEnlazada()

        self.resaltados = set()
        self.registros = []

        self.ventana_historial = None
        self.lista_historial = None

        ventana.title(
            "LinkedList Studio | Nodos y conexiones"
        )
        ventana.geometry("1210x770")
        ventana.minsize(870, 620)
        ventana.configure(bg=FONDO)

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "TEntry",
            fieldbackground=LILA_CLARO,
            foreground="#2E1065",
            padding=5
        )

        estilo.configure(
            "TCombobox",
            fieldbackground=LILA_CLARO,
            foreground="#2E1065",
            padding=5
        )

        self.construir()

        self.registrar(
            "INICIO",
            "Aplicación iniciada"
        )

        self.actualizar()

    # ==========================================
    # BOTONES
    # ==========================================

    def boton(self, padre, texto, accion, color=MORADO):
        return tk.Button(
            padre,
            text=texto,
            command=accion,
            bg=color,
            fg="white",
            activebackground=MORADO_OSCURO,
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10,
            pady=8,
            cursor="hand2"
        )

    def etiqueta(self, padre, texto, fila, columna):
        tk.Label(
            padre,
            text=texto,
            bg=PANEL,
            fg=TEXTO,
            font=("Segoe UI", 10)
        ).grid(
            row=fila,
            column=columna,
            padx=5,
            sticky="w"
        )

    # ==========================================
    # CONSTRUIR INTERFAZ
    # ==========================================

    def construir(self):
        cabecera = tk.Frame(
            self.ventana,
            bg=FONDO,
            padx=18,
            pady=13
        )
        cabecera.pack(fill="x")

        tk.Label(
            cabecera,
            text="⛓ LinkedList Studio",
            fg=LILA,
            bg=FONDO,
            font=("Segoe UI", 23, "bold")
        ).pack(side="left")

        self.boton(
            cabecera,
            "Historial separado",
            self.abrir_historial,
            MORADO_OSCURO
        ).pack(side="right")

        # PANEL DE OPERACIONES
        panel = tk.Frame(
            self.ventana,
            bg=PANEL,
            padx=12,
            pady=10
        )
        panel.pack(
            fill="x",
            padx=14,
            pady=6
        )

        self.etiqueta(panel, "Dato", 0, 0)
        self.etiqueta(panel, "Insertar", 0, 1)
        self.etiqueta(panel, "Posición", 0, 2)

        self.entrada_dato = ttk.Entry(
            panel,
            width=14
        )
        self.entrada_dato.grid(
            row=1, column=0, padx=5
        )

        self.operacion = ttk.Combobox(
            panel,
            width=17,
            state="readonly",
            values=[
                "Al inicio",
                "Al final",
                "En una posición"
            ]
        )

        self.operacion.current(0)
        self.operacion.grid(
            row=1, column=1, padx=5
        )

        self.entrada_posicion = ttk.Entry(
            panel,
            width=10
        )
        self.entrada_posicion.grid(
            row=1, column=2, padx=5
        )

        self.boton(
            panel,
            "Insertar",
            self.insertar
        ).grid(row=1, column=3, padx=4)

        self.boton(
            panel,
            "Buscar dato",
            self.buscar,
            "#6D28D9"
        ).grid(row=1, column=4, padx=4)

        self.boton(
            panel,
            "Eliminar posición",
            self.eliminar,
            ROJO
        ).grid(row=1, column=5, padx=4)

        self.boton(
            panel,
            "Limpiar",
            self.limpiar,
            PANEL_CLARO
        ).grid(row=1, column=6, padx=4)

        self.ayuda = tk.Label(
            panel,
            text="",
            bg=PANEL,
            fg=TEXTO_SECUNDARIO,
            font=("Segoe UI", 9)
        )

        self.ayuda.grid(
            row=2,
            column=0,
            columnspan=7,
            sticky="w",
            pady=(9, 0)
        )

        self.operacion.bind(
            "<<ComboboxSelected>>",
            lambda _: self.actualizar_ayuda()
        )

        # PANEL DE CONEXIONES
        links = tk.LabelFrame(
            self.ventana,
            text="Conexiones: reemplazar la secuencia",
            bg=PANEL,
            fg=LILA,
            padx=12,
            pady=9,
            font=("Segoe UI", 11, "bold")
        )

        links.pack(
            fill="x",
            padx=14,
            pady=8
        )

        self.etiqueta(links, "ID origen", 0, 0)

        self.origen = ttk.Entry(
            links,
            width=9
        )
        self.origen.grid(
            row=0, column=1, padx=5
        )

        self.etiqueta(links, "ID destino", 0, 2)

        self.destino = ttk.Entry(
            links,
            width=9
        )
        self.destino.grid(
            row=0, column=3, padx=5
        )

        self.boton(
            links,
            "Conectar / sustituir",
            self.conectar
        ).grid(
            row=0, column=4, padx=5
        )

        self.boton(
            links,
            "Quitar conexión del origen",
            self.desconectar,
            PANEL_CLARO
        ).grid(
            row=0, column=5, padx=5
        )

        tk.Label(
            links,
            text=(
                "Usa los ID sobre cada nodo. "
                "Dos nodos pueden apuntar al mismo destino."
            ),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO,
            font=("Segoe UI", 9)
        ).grid(
            row=1,
            column=0,
            columnspan=6,
            sticky="w",
            pady=(8, 0)
        )

        # ÁREA DE VISUALIZACIÓN
        tk.Label(
            self.ventana,
            text=(
                "Vista de los nodos "
                "(las flechas son las ligas reales)"
            ),
            bg=FONDO,
            fg=TEXTO,
            font=("Segoe UI", 14, "bold")
        ).pack(
            anchor="w",
            padx=14,
            pady=(8, 5)
        )

        lienzo = tk.Frame(
            self.ventana,
            bg=FONDO
        )
        lienzo.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=4
        )

        self.canvas = tk.Canvas(
            lienzo,
            bg=LILA_CLARO,
            highlightthickness=0
        )

        horizontal = ttk.Scrollbar(
            lienzo,
            orient="horizontal",
            command=self.canvas.xview
        )

        vertical = ttk.Scrollbar(
            lienzo,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            xscrollcommand=horizontal.set,
            yscrollcommand=vertical.set
        )

        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        horizontal.grid(
            row=1, column=0, sticky="ew"
        )

        vertical.grid(
            row=0, column=1, sticky="ns"
        )

        lienzo.grid_rowconfigure(0, weight=1)
        lienzo.grid_columnconfigure(0, weight=1)

        self.estado = tk.Label(
            self.ventana,
            bg=FONDO,
            fg=LILA,
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        )

        self.estado.pack(
            fill="x",
            padx=14,
            pady=(2, 10)
        )

    # ==========================================
    # HISTORIAL DE OPERACIONES
    # ==========================================

    def registrar(self, accion, detalle):
        registro = (
            f"[{datetime.now():%H:%M:%S}] "
            f"{accion}: {detalle}"
        )

        self.registros.append(registro)

        if (
            self.ventana_historial is not None
            and self.ventana_historial.winfo_exists()
        ):
            self.lista_historial.insert(
                tk.END,
                registro
            )
            self.lista_historial.see(tk.END)

    def registrar_extremos(self):
        ruta = self.lista.recorrido()

        if not ruta:
            self.registrar(
                "ESTADO",
                "Sin nodos alcanzables"
            )
        else:
            self.registrar(
                "EXTREMOS",
                f"Primero={ruta[0].dato}; "
                f"último visible={ruta[-1].dato}"
            )

    def abrir_historial(self):
        if (
            self.ventana_historial is not None
            and self.ventana_historial.winfo_exists()
        ):
            self.ventana_historial.lift()
            return

        v = tk.Toplevel(self.ventana)
        self.ventana_historial = v

        v.title("Historial | LinkedList Studio")
        v.geometry("820x440")
        v.configure(bg=FONDO)

        tk.Label(
            v,
            text="Historial de operaciones",
            bg=FONDO,
            fg=LILA,
            font=("Segoe UI", 19, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=12
        )

        marco = tk.Frame(
            v,
            bg=PANEL
        )
        marco.pack(
            fill="both",
            expand=True,
            padx=15
        )

        self.lista_historial = tk.Listbox(
            marco,
            bg=PANEL,
            fg=TEXTO,
            font=("Consolas", 10),
            relief="flat",
            selectbackground=MORADO
        )

        self.lista_historial.pack(
            side="left",
            fill="both",
            expand=True
        )

        sb = ttk.Scrollbar(
            marco,
            command=self.lista_historial.yview
        )
        sb.pack(
            side="right",
            fill="y"
        )

        self.lista_historial.configure(
            yscrollcommand=sb.set
        )

        for registro in self.registros:
            self.lista_historial.insert(
                tk.END,
                registro
            )

        self.lista_historial.see(tk.END)

        pie = tk.Frame(
            v,
            bg=FONDO
        )
        pie.pack(
            fill="x",
            padx=15,
            pady=12
        )

        self.boton(
            pie,
            "Borrar historial",
            self.borrar_historial,
            ROJO
        ).pack(side="left")

        self.boton(
            pie,
            "Cerrar",
            v.destroy,
            MORADO_OSCURO
        ).pack(side="right")

    def borrar_historial(self):
        self.registros.clear()

        if (
            self.ventana_historial is not None
            and self.ventana_historial.winfo_exists()
        ):
            self.lista_historial.delete(
                0,
                tk.END
            )

        self.registrar(
            "HISTORIAL",
            "Se borraron los registros anteriores"
        )

    # ==========================================
    # VALIDACIÓN DE NÚMEROS
    # ==========================================

    def leer_entero(self, entrada, nombre):
        valor = entrada.get().strip()

        if not valor:
            raise ValueError(
                f"Escribe {nombre}."
            )

        try:
            return int(valor)
        except ValueError:
            raise ValueError(
                f"{nombre.capitalize()} "
                "debe ser un número entero."
            )

    # ==========================================
    # INSERTAR
    # ==========================================

    def insertar(self):
        try:
            dato = self.leer_entero(
                self.entrada_dato,
                "un dato"
            )

            modo = self.operacion.get()

            if modo == "Al inicio":
                nodo = self.lista.insertar_inicio(dato)

            elif modo == "Al final":
                nodo = self.lista.insertar_final(dato)

            else:
                posicion = self.leer_entero(
                    self.entrada_posicion,
                    "una posición"
                )

                nodo = self.lista.insertar_posicion(
                    dato,
                    posicion
                )

            self.resaltados = {nodo.id}

            self.registrar(
                "INSERCIÓN",
                f"Dato={dato}, "
                f"ID={nodo.id}, modo={modo}"
            )

            self.registrar_extremos()

            self.entrada_dato.delete(
                0,
                tk.END
            )

            self.actualizar()

        except ValueError as error:
            messagebox.showerror(
                "No se pudo insertar",
                str(error)
            )

    # ==========================================
    # BUSCAR
    # ==========================================

    def buscar(self):
        try:
            dato = self.leer_entero(
                self.entrada_dato,
                "un dato"
            )

            resultados = self.lista.buscar(dato)

            self.resaltados = {
                n.id for _, n in resultados
            }

            if resultados:
                posiciones = ", ".join(
                    str(p)
                    for p, _ in resultados
                )

                self.registrar(
                    "BÚSQUEDA",
                    f"Dato={dato}, posiciones={posiciones}"
                )

                messagebox.showinfo(
                    "Búsqueda",
                    f"{dato} aparece en las "
                    f"posiciones: {posiciones}."
                )

            else:
                self.registrar(
                    "BÚSQUEDA",
                    f"Dato={dato}, "
                    "no encontrado desde INICIO"
                )

                messagebox.showinfo(
                    "Búsqueda",
                    f"No se encontró {dato} "
                    "desde INICIO."
                )

            self.actualizar()

        except ValueError as error:
            messagebox.showerror(
                "Búsqueda",
                str(error)
            )

    # ==========================================
    # ELIMINAR
    # ==========================================

    def eliminar(self):
        try:
            posicion = self.leer_entero(
                self.entrada_posicion,
                "una posición"
            )

            eliminado = self.lista.eliminar_posicion(
                posicion
            )

            self.resaltados.clear()

            self.registrar(
                "ELIMINACIÓN",
                f"Dato={eliminado.dato}, "
                f"ID={eliminado.id}, "
                f"posición={posicion}"
            )

            self.registrar_extremos()
            self.actualizar()

        except ValueError as error:
            messagebox.showerror(
                "No se pudo eliminar",
                str(error)
            )

    # ==========================================
    # CONECTAR NODOS
    # ==========================================

    def conectar(self):
        try:
            origen = self.leer_entero(
                self.origen,
                "el ID de origen"
            )

            destino = self.leer_entero(
                self.destino,
                "el ID de destino"
            )

            a, b = self.lista.conectar(
                origen,
                destino
            )

            self.resaltados = {
                a.id,
                b.id
            }

            self.registrar(
                "CONEXIÓN",
                f"ID {a.id} apunta a ID {b.id}; "
                "enlace previo reemplazado"
            )

            self.registrar_extremos()
            self.actualizar()

        except ValueError as error:
            messagebox.showerror(
                "No se pudo conectar",
                str(error)
            )

    # ==========================================
    # DESCONECTAR
    # ==========================================

    def desconectar(self):
        try:
            origen = self.leer_entero(
                self.origen,
                "el ID de origen"
            )

            nodo = self.lista.desconectar(origen)

            self.resaltados = {nodo.id}

            self.registrar(
                "DESCONEXIÓN",
                f"ID {origen} ahora apunta a None"
            )

            self.registrar_extremos()
            self.actualizar()

        except ValueError as error:
            messagebox.showerror(
                "No se pudo desconectar",
                str(error)
            )

    # ==========================================
    # LIMPIAR
    # ==========================================

    def limpiar(self):
        if not self.lista.nodos:
            messagebox.showinfo(
                "Lista vacía",
                "No hay nodos que eliminar."
            )
            return

        if not messagebox.askyesno(
            "Limpiar lista",
            "¿Eliminar todos los nodos?"
        ):
            return

        cuantos = len(self.lista.nodos)

        self.lista.limpiar()
        self.resaltados.clear()

        self.registrar(
            "LIMPIEZA",
            f"Se eliminaron {cuantos} nodos"
        )

        self.registrar_extremos()
        self.actualizar()

    # ==========================================
    # AYUDA DE POSICIONES
    # ==========================================

    def actualizar_ayuda(self):
        cantidad = self.lista.cantidad()

        if self.operacion.get() == "Al inicio":
            msg = "Se insertará antes del primer nodo."

        elif self.operacion.get() == "Al final":
            msg = (
                "Se insertará después del último nodo "
                "(si no hay ciclo)."
            )

        else:
            msg = (
                "Posiciones disponibles desde INICIO: "
                f"1 a {cantidad + 1}."
            )

        self.ayuda.configure(text=msg)

    # ==========================================
    # ACTUALIZAR REPRESENTACIÓN VISUAL
    # ==========================================

    def actualizar(self):
        self.canvas.delete("all")

        ruta = self.lista.recorrido()

        activos = {
            n.id for n in ruta
        }

        restantes = [
            n for n in self.lista.nodos.values()
            if n.id not in activos
        ]

        todos = ruta + restantes

        if not todos:
            self.canvas.create_text(
                320,
                150,
                text=(
                    "La lista está vacía\n"
                    "Inserta un número"
                ),
                fill=MORADO_OSCURO,
                font=("Segoe UI", 17),
                justify="center"
            )

            self.canvas.configure(
                scrollregion=(0, 0, 800, 340)
            )

            self.estado.configure(
                text="Total de nodos: 0"
            )

            self.actualizar_ayuda()
            return

        ancho = 110
        alto = 66
        salto = 180

        posiciones = {}

        # ======================================
        # DIBUJAR NODOS
        # ======================================

        grupos = [
            ("RUTA DESDE INICIO", ruta, 160),
            ("NODOS DESCONECTADOS", restantes, 360)
        ]

        for grupo, nodos, centro_y in grupos:
            if not nodos:
                continue

            self.canvas.create_text(
                25,
                centro_y - 90,
                text=grupo,
                anchor="w",
                fill="#6D28D9",
                font=("Segoe UI", 10, "bold")
            )

            for i, nodo in enumerate(nodos):
                x = 30 + i * salto
                y = centro_y - alto / 2

                posiciones[nodo.id] = (x, y)

                seleccionado = (
                    nodo.id in self.resaltados
                )

                borde = (
                    MORADO
                    if seleccionado
                    else "#A78BFA"
                )

                relleno = (
                    LILA_SELECCION
                    if seleccionado
                    else "#F5F3FF"
                )

                # RECTÁNGULO DEL NODO
                self.canvas.create_rectangle(
                    x,
                    y,
                    x + ancho,
                    y + alto,
                    fill=relleno,
                    outline=borde,
                    width=3 if seleccionado else 2
                )

                # SEPARADOR DATO - LIGA
                self.canvas.create_line(
                    x + 74,
                    y,
                    x + 74,
                    y + alto,
                    fill=borde,
                    width=2
                )

                # DATO
                self.canvas.create_text(
                    x + 37,
                    centro_y,
                    text=str(nodo.dato),
                    fill="#4C1D95",
                    font=("Segoe UI", 15, "bold")
                )

                # LIGA
                self.canvas.create_text(
                    x + 92,
                    centro_y,
                    text="liga",
                    fill="#6D28D9",
                    font=("Segoe UI", 9)
                )

                # ID DEL NODO
                self.canvas.create_text(
                    x + ancho / 2,
                    y - 17,
                    text=f"ID {nodo.id}",
                    fill="#4C1D95",
                    font=("Segoe UI", 10, "bold")
                )

        # ======================================
        # DIBUJAR CONEXIONES REALES
        # ======================================

        for nodo in todos:
            x, y = posiciones[nodo.id]

            # Nodo sin conexión
            if nodo.liga is None:
                self.canvas.create_line(
                    x + ancho,
                    y + alto / 2,
                    x + ancho + 30,
                    y + alto / 2,
                    fill="#8B5CF6",
                    width=2,
                    arrow=tk.LAST
                )

                self.canvas.create_text(
                    x + ancho + 33,
                    y + alto / 2,
                    text="None",
                    anchor="w",
                    fill=MORADO_OSCURO,
                    font=("Segoe UI", 9)
                )

                continue

            dest = posiciones.get(nodo.liga.id)

            if dest is None:
                continue

            dx, dy = dest

            vecino = (
                abs(dx - x - salto) < 1
                and abs(dy - y) < 1
            )

            # CONEXIÓN NORMAL
            if vecino:
                self.canvas.create_line(
                    x + ancho,
                    y + alto / 2,
                    dx,
                    dy + alto / 2,
                    fill=MORADO,
                    width=3,
                    arrow=tk.LAST
                )

            # CONEXIÓN QUE SALTA NODOS
            else:
                altura = (
                    min(y, dy)
                    - 55
                    - 18 * (nodo.id % 3)
                )

                self.canvas.create_line(
                    x + ancho / 2,
                    y,
                    x + ancho / 2,
                    altura,
                    dx + ancho / 2,
                    altura,
                    dx + ancho / 2,
                    dy,
                    smooth=True,
                    splinesteps=28,
                    fill="#9333EA",
                    width=3,
                    dash=(7, 4),
                    arrow=tk.LAST
                )

        # ======================================
        # AJUSTAR ÁREA VISUAL
        # ======================================

        total_ancho = max(
            850,
            220 + max(
                len(ruta),
                len(restantes)
            ) * salto
        )

        alto_total = (
            510 if restantes else 300
        )

        self.canvas.configure(
            scrollregion=(
                0,
                0,
                total_ancho,
                alto_total
            )
        )

        # ======================================
        # ESTADO DE LA LISTA
        # ======================================

        datos = [
            n.dato for n in ruta
        ]

        primero = (
            str(datos[0])
            if datos else "—"
        )

        ultimo = (
            str(datos[-1])
            if datos else "—"
        )

        ciclo = (
            "Sí"
            if self.lista.hay_ciclo()
            else "No"
        )

        self.estado.configure(
            text=(
                f"Nodos totales: {len(todos)}"
                f"   |   Alcanzables: {len(ruta)}"
                f"   |   Desconectados: {len(restantes)}"
                f"   |   Primero: {primero}"
                f"   |   Último visible: {ultimo}"
                f"   |   Ciclo: {ciclo}"
            )
        )

        self.actualizar_ayuda()


# ==========================================
# EJECUCIÓN DEL PROGRAMA
# ==========================================

if __name__ == "__main__":
    ventana = tk.Tk()
    app = Aplicacion(ventana)
    ventana.mainloop()
