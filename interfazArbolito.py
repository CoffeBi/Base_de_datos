
import tkinter as tk
from tkinter import ttk, messagebox
from arbolito import Arbol


# COLORES
BG = "#111827"
PANEL = "#1F2937"
INPUT = "#374151"
TEXT = "#F9FAFB"
MUTED = "#9CA3AF"
ACCENT = "#3B82F6"
SUCCESS = "#10B981"
DANGER = "#EF4444"
WARNING = "#F59E0B"
LINE = "#64748B"


class InterfazArbol:
    def __init__(self, root):
        self.root = root
        self.root.title("Árbol Binario de Búsqueda")
        self.root.geometry("1100x720")
        self.root.minsize(800, 580)
        self.root.configure(bg=BG)

        self.arbol = Arbol()
        self.resaltado = None

        self.crear_interfaz()
        self.actualizar_arbol()

    def crear_interfaz(self):
        # CONTENEDOR PRINCIPAL
        principal = tk.Frame(self.root, bg=BG)
        principal.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        # Distribución vertical flexible
        principal.grid_columnconfigure(0, weight=1)
        principal.grid_rowconfigure(3, weight=1)

        # ENCABEZADO
        encabezado = tk.Frame(principal, bg=BG)
        encabezado.grid(
            row=0, column=0,
            sticky="ew",
            pady=(0, 12)
        )

        tk.Label(
            encabezado,
            text="Árbol Binario de Búsqueda",
            font=("Arial", 20, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w")

        tk.Label(
            encabezado,
            text="Gestión y visualización de árboles binarios",
            font=("Arial", 10),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", pady=(3, 0))

        # PANEL DE OPERACIONES
        operaciones = tk.Frame(
            principal,
            bg=PANEL,
            padx=15,
            pady=12
        )
        operaciones.grid(
            row=1, column=0,
            sticky="ew",
            pady=(0, 10)
        )

        operaciones.grid_columnconfigure(0, weight=1)

        fila_entrada = tk.Frame(operaciones, bg=PANEL)
        fila_entrada.grid(
            row=0, column=0,
            sticky="w",
            pady=(0, 10)
        )

        tk.Label(
            fila_entrada,
            text="Valor del nodo:",
            bg=PANEL,
            fg=TEXT,
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=(0, 10))

        self.entrada = tk.Entry(
            fila_entrada,
            width=15,
            font=("Arial", 12),
            bg=INPUT,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            justify="center"
        )
        self.entrada.pack(
            side="left",
            ipady=5
        )
        self.entrada.bind(
            "<Return>",
            lambda e: self.insertar()
        )

        fila_botones = tk.Frame(
            operaciones, bg=PANEL
        )
        fila_botones.grid(
            row=1, column=0,
            sticky="ew"
        )

        botones_config = [
            ("Insertar", self.insertar, SUCCESS),
            ("Buscar", self.buscar, ACCENT),
            ("Eliminar", self.eliminar, DANGER),
            ("Vaciar árbol", self.vaciar, INPUT)
        ]

        for i, (texto, comando, color) in enumerate(
            botones_config
        ):
            fila_botones.grid_columnconfigure(
                i, weight=1, uniform="botones"
            )

            boton = self.crear_boton(
                fila_botones, texto, comando, color
            )
            boton.grid(
                row=0,
                column=i,
                sticky="ew",
                padx=4
            )

        # INFORMACIÓN DEL ÁRBOL
        informacion = tk.Frame(principal, bg=BG)
        informacion.grid(
            row=2, column=0,
            sticky="ew",
            pady=(0, 10)
        )

        self.lbl_nodos = tk.Label(
            informacion,
            text="Nodos: 0",
            bg=BG,
            fg=TEXT,
            font=("Arial", 11, "bold")
        )
        self.lbl_nodos.pack(side="left")

        self.lbl_altura = tk.Label(
            informacion,
            text="Altura: 0",
            bg=BG,
            fg=TEXT,
            font=("Arial", 11, "bold")
        )
        self.lbl_altura.pack(
            side="left",
            padx=30
        )

        # PANEL DE VISUALIZACIÓN
        panel_arbol = tk.Frame(
            principal,
            bg=PANEL
        )
        panel_arbol.grid(
            row=3,
            column=0,
            sticky="nsew",
            pady=(0, 10)
        )

        panel_arbol.grid_columnconfigure(
            0, weight=1
        )
        panel_arbol.grid_rowconfigure(
            1, weight=1
        )

        tk.Label(
            panel_arbol,
            text="Visualización del árbol",
            bg=PANEL,
            fg=TEXT,
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=10
        )

        area = tk.Frame(panel_arbol, bg=PANEL)
        area.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        area.grid_columnconfigure(0, weight=1)
        area.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            area,
            bg=PANEL,
            highlightthickness=0
        )
        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.scroll_y = ttk.Scrollbar(
            area,
            orient="vertical",
            command=self.canvas.yview
        )
        self.scroll_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.scroll_x = ttk.Scrollbar(
            area,
            orient="horizontal",
            command=self.canvas.xview
        )
        self.scroll_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.canvas.configure(
            xscrollcommand=self.scroll_x.set,
            yscrollcommand=self.scroll_y.set
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.actualizar_arbol()
        )

        # PANEL DE RECORRIDOS
        panel_recorridos = tk.Frame(
            principal,
            bg=PANEL,
            padx=15,
            pady=10
        )
        panel_recorridos.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(0, 8)
        )

        tk.Label(
            panel_recorridos,
            text="Recorridos del árbol",
            font=("Arial", 12, "bold"),
            bg=PANEL,
            fg=TEXT
        ).pack(anchor="w", pady=(0, 8))

        fila_recorridos = tk.Frame(
            panel_recorridos,
            bg=PANEL
        )
        fila_recorridos.pack(fill="x")

        recorridos = [
            ("Preorden", "Preorden"),
            ("Inorden", "Inorden"),
            ("Postorden", "Postorden")
        ]

        for i, (texto, tipo) in enumerate(recorridos):
            fila_recorridos.grid_columnconfigure(
                i, weight=1, uniform="recorridos"
            )

            boton = self.crear_boton(
                fila_recorridos,
                texto,
                lambda t=tipo: self.mostrar_recorrido(t),
                ACCENT
            )
            boton.grid(
                row=0,
                column=i,
                sticky="ew",
                padx=4
            )

        self.lbl_recorrido = tk.Label(
            panel_recorridos,
            text="Selecciona un recorrido para visualizarlo.",
            bg=PANEL,
            fg=MUTED,
            font=("Arial", 10),
            anchor="w",
            justify="left"
        )
        self.lbl_recorrido.pack(
            fill="x",
            pady=(10, 0)
        )

        # BARRA DE ESTADO
        self.estado = tk.Label(
            principal,
            text="Programa listo.",
            bg=BG,
            fg=SUCCESS,
            font=("Arial", 10),
            anchor="w"
        )
        self.estado.grid(
            row=5,
            column=0,
            sticky="ew"
        )

    def crear_boton(self, padre, texto, comando, color):
        return tk.Button(
            padre,
            text=texto,
            command=comando,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=7,
            borderwidth=0
        )

    def obtener_valor(self):
        texto = self.entrada.get().strip()

        if not texto:
            self.mostrar_estado(
                "Ingresa un número entero.", DANGER
            )
            return None

        try:
            return int(texto)
        except ValueError:
            self.mostrar_estado(
                "Solo se permiten números enteros.",
                DANGER
            )
            return None

    def mostrar_estado(self, mensaje, color=SUCCESS):
        self.estado.config(text=mensaje, fg=color)

    def insertar(self):
        valor = self.obtener_valor()

        if valor is None:
            return

        if self.arbol.insertar(valor):
            self.resaltado = valor
            self.mostrar_estado(
                f"Nodo {valor} insertado correctamente."
            )
        else:
            self.mostrar_estado(
                f"El nodo {valor} ya existe.",
                WARNING
            )

        self.entrada.delete(0, tk.END)
        self.actualizar_arbol()

    def buscar(self):
        valor = self.obtener_valor()

        if valor is None:
            return

        if self.arbol.buscar(valor):
            self.resaltado = valor
            self.mostrar_estado(
                f"Nodo {valor} encontrado.",
                SUCCESS
            )
        else:
            self.resaltado = None
            self.mostrar_estado(
                f"El nodo {valor} no existe.",
                DANGER
            )

        self.actualizar_arbol()

    def eliminar(self):
        valor = self.obtener_valor()

        if valor is None:
            return

        if self.arbol.eliminar(valor):
            self.resaltado = None
            self.mostrar_estado(
                f"Nodo {valor} eliminado correctamente."
            )
        else:
            self.mostrar_estado(
                f"El nodo {valor} no existe.",
                DANGER
            )

        self.entrada.delete(0, tk.END)
        self.actualizar_arbol()

    def vaciar(self):
        if self.arbol.raiz is None:
            self.mostrar_estado(
                "El árbol ya está vacío.",
                WARNING
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Deseas eliminar todos los nodos?"
        )

        if confirmar:
            self.arbol.vaciar()
            self.resaltado = None

            self.lbl_recorrido.config(
                text="Selecciona un recorrido para visualizarlo."
            )

            self.actualizar_arbol()
            self.mostrar_estado(
                "Árbol vaciado correctamente."
            )

    def mostrar_recorrido(self, tipo):
        if tipo == "Preorden":
            valores = self.arbol.preorden()
        elif tipo == "Inorden":
            valores = self.arbol.inorden()
        else:
            valores = self.arbol.postorden()

        if not valores:
            self.lbl_recorrido.config(
                text="El árbol está vacío."
            )
            return

        resultado = " → ".join(map(str, valores))

        self.lbl_recorrido.config(
            text=f"{tipo}: {resultado}"
        )

        self.mostrar_estado(
            f"Recorrido {tipo.lower()} realizado."
        )

    def actualizar_arbol(self):
        self.canvas.delete("all")

        cantidad = self.arbol.contar_nodos()
        altura = self.arbol.altura()

        self.lbl_nodos.config(
            text=f"Nodos: {cantidad}"
        )
        self.lbl_altura.config(
            text=f"Altura: {altura}"
        )

        ancho_visible = max(
            self.canvas.winfo_width(), 300
        )
        alto_visible = max(
            self.canvas.winfo_height(), 150
        )

        if self.arbol.raiz is None:
            self.canvas.configure(
                scrollregion=(
                    0, 0,
                    ancho_visible,
                    alto_visible
                )
            )

            self.canvas.create_text(
                ancho_visible / 2,
                alto_visible / 2,
                text=(
                    "El árbol está vacío\n"
                    "Inserta un nodo para comenzar"
                ),
                fill=MUTED,
                font=("Arial", 13),
                justify="center"
            )
            return

        posiciones = {}
        contador = [0]

        # ASIGNAR POSICIONES POR INORDEN
        def asignar_posiciones(nodo, nivel):
            if nodo is None:
                return

            asignar_posiciones(
                nodo.izquierdo, nivel + 1
            )

            indice = contador[0]
            contador[0] += 1

            posiciones[nodo] = (
                indice * 85,
                45 + nivel * 90
            )

            asignar_posiciones(
                nodo.derecho, nivel + 1
            )

        asignar_posiciones(self.arbol.raiz, 0)

        ancho_arbol = max(
            0, (cantidad - 1) * 85
        )

        ancho_total = max(
            ancho_visible,
            ancho_arbol + 100
        )

        alto_total = max(
            alto_visible,
            altura * 90 + 70
        )

        desplazamiento = (
            ancho_total - ancho_arbol
        ) / 2

        def coordenadas(nodo):
            x, y = posiciones[nodo]
            return (
                x + desplazamiento,
                y
            )

        # DIBUJAR CONEXIONES
        def dibujar_lineas(nodo):
            if nodo is None:
                return

            x, y = coordenadas(nodo)

            if nodo.izquierdo is not None:
                x2, y2 = coordenadas(
                    nodo.izquierdo
                )

                self.canvas.create_line(
                    x, y, x2, y2,
                    fill=LINE,
                    width=3
                )

                dibujar_lineas(nodo.izquierdo)

            if nodo.derecho is not None:
                x2, y2 = coordenadas(
                    nodo.derecho
                )

                self.canvas.create_line(
                    x, y, x2, y2,
                    fill=LINE,
                    width=3
                )

                dibujar_lineas(nodo.derecho)

        # DIBUJAR NODOS
        def dibujar_nodos(nodo):
            if nodo is None:
                return

            x, y = coordenadas(nodo)
            radio = 23

            if nodo.dato == self.resaltado:
                color = SUCCESS

            elif nodo == self.arbol.raiz:
                color = WARNING

            else:
                color = ACCENT

            self.canvas.create_oval(
                x - radio,
                y - radio,
                x + radio,
                y + radio,
                fill=color,
                outline=TEXT,
                width=2
            )

            self.canvas.create_text(
                x, y,
                text=str(nodo.dato),
                fill="white",
                font=("Arial", 10, "bold")
            )

            dibujar_nodos(nodo.izquierdo)
            dibujar_nodos(nodo.derecho)

        dibujar_lineas(self.arbol.raiz)
        dibujar_nodos(self.arbol.raiz)

        self.canvas.configure(
            scrollregion=(
                0, 0,
                ancho_total,
                alto_total
            )
        )

        # CENTRAR EL ÁRBOL
        if ancho_total > ancho_visible:
            fraccion_x = (
                (ancho_total - ancho_visible) / 2
            ) / ancho_total

            self.canvas.xview_moveto(fraccion_x)
        else:
            self.canvas.xview_moveto(0)

        self.canvas.yview_moveto(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazArbol(root)
    root.mainloop()
