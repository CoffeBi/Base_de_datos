
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# IMPORTAR NUESTRA PROPIA BIBLIOTECA
from lista_enlazada import ListaEnlazada


# ==========================================
# PALETA DE COLORES MORADOS
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
BLANCO = "#FFFFFF"


# ==========================================
# INTERFAZ GRÁFICA
# ==========================================

class Aplicacion:

    def __init__(self, ventana):

        self.ventana = ventana

        # Instancia de nuestra biblioteca
        self.lista = ListaEnlazada()

        self.resaltados = set()
        self.registros = []

        self.ventana_historial = None
        self.lista_historial = None

        ventana.title(
            "LinkedList Studio | Mi propia biblioteca"
        )
        ventana.geometry("1250x800")
        ventana.minsize(900, 620)
        ventana.configure(bg=FONDO)

        self.configurar_estilos()
        self.crear_interfaz()

        self.registrar(
            "INICIO",
            "Aplicación iniciada usando lista_enlazada.py"
        )

        self.actualizar_lista()

    # ======================================
    # CONFIGURAR ESTILOS
    # ======================================

    def configurar_estilos(self):

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "TEntry",
            fieldbackground=LILA_CLARO,
            foreground="#2E1065",
            padding=6
        )

        estilo.configure(
            "TCombobox",
            fieldbackground=LILA_CLARO,
            foreground="#2E1065",
            padding=6
        )

    def crear_boton(self, padre, texto, comando, color):

        return tk.Button(
            padre,
            text=texto,
            command=comando,
            bg=color,
            fg=BLANCO,
            activebackground=MORADO_OSCURO,
            activeforeground=BLANCO,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=9
        )

    # ======================================
    # CREAR INTERFAZ
    # ======================================

    def crear_interfaz(self):

        # ENCABEZADO
        encabezado = tk.Frame(
            self.ventana,
            bg=FONDO,
            padx=20,
            pady=15
        )
        encabezado.pack(fill="x")

        tk.Label(
            encabezado,
            text="⛓ LinkedList Studio",
            font=("Segoe UI", 25, "bold"),
            bg=FONDO,
            fg=LILA
        ).pack(side="left")

        self.crear_boton(
            encabezado,
            "Historial",
            self.abrir_historial,
            MORADO_OSCURO
        ).pack(side="right")

        # PANEL PRINCIPAL
        panel = tk.LabelFrame(
            self.ventana,
            text="Operaciones con nodos",
            bg=PANEL,
            fg=LILA,
            font=("Segoe UI", 11, "bold"),
            padx=12,
            pady=12
        )

        panel.pack(
            fill="x",
            padx=15,
            pady=8
        )

        tk.Label(
            panel,
            text="Dato:",
            bg=PANEL,
            fg=TEXTO
        ).grid(row=0, column=0, sticky="w")

        self.entrada_dato = ttk.Entry(
            panel,
            width=14
        )
        self.entrada_dato.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        tk.Label(
            panel,
            text="Operación:",
            bg=PANEL,
            fg=TEXTO
        ).grid(row=0, column=1, sticky="w")

        self.operacion = ttk.Combobox(
            panel,
            values=[
                "Al inicio",
                "Al final",
                "En una posición"
            ],
            state="readonly",
            width=17
        )

        self.operacion.current(0)
        self.operacion.grid(
            row=1,
            column=1,
            padx=5
        )

        tk.Label(
            panel,
            text="Posición:",
            bg=PANEL,
            fg=TEXTO
        ).grid(row=0, column=2, sticky="w")

        self.entrada_posicion = ttk.Entry(
            panel,
            width=10
        )
        self.entrada_posicion.grid(
            row=1,
            column=2,
            padx=5
        )

        self.crear_boton(
            panel,
            "Insertar",
            self.insertar,
            MORADO
        ).grid(row=1, column=3, padx=4)

        self.crear_boton(
            panel,
            "Buscar",
            self.buscar,
            "#6D28D9"
        ).grid(row=1, column=4, padx=4)

        self.crear_boton(
            panel,
            "Eliminar",
            self.eliminar,
            ROJO
        ).grid(row=1, column=5, padx=4)

        self.crear_boton(
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
            pady=10
        )

        self.operacion.bind(
            "<<ComboboxSelected>>",
            lambda evento: self.actualizar_ayuda()
        )

        # PANEL DE CONEXIONES
        conexiones = tk.LabelFrame(
            self.ventana,
            text="Conexiones entre nodos",
            bg=PANEL,
            fg=LILA,
            font=("Segoe UI", 11, "bold"),
            padx=12,
            pady=12
        )

        conexiones.pack(
            fill="x",
            padx=15,
            pady=8
        )

        tk.Label(
            conexiones,
            text="ID origen:",
            bg=PANEL,
            fg=TEXTO
        ).grid(row=0, column=0, padx=5)

        self.entrada_origen = ttk.Entry(
            conexiones,
            width=10
        )
        self.entrada_origen.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Label(
            conexiones,
            text="ID destino:",
            bg=PANEL,
            fg=TEXTO
        ).grid(row=0, column=2, padx=5)

        self.entrada_destino = ttk.Entry(
            conexiones,
            width=10
        )
        self.entrada_destino.grid(
            row=0,
            column=3,
            padx=5
        )

        self.crear_boton(
            conexiones,
            "Conectar nodos",
            self.conectar,
            MORADO
        ).grid(row=0, column=4, padx=5)

        self.crear_boton(
            conexiones,
            "Desconectar",
            self.desconectar,
            PANEL_CLARO
        ).grid(row=0, column=5, padx=5)

        tk.Label(
            conexiones,
            text=(
                "Las conexiones se realizan con los ID "
                "de los nodos, no con sus posiciones."
            ),
            bg=PANEL,
            fg=TEXTO_SECUNDARIO
        ).grid(
            row=1,
            column=0,
            columnspan=6,
            sticky="w",
            pady=10
        )

        # REPRESENTACIÓN VISUAL
        tk.Label(
            self.ventana,
            text="Representación visual de los nodos",
            font=("Segoe UI", 15, "bold"),
            bg=FONDO,
            fg=TEXTO
        ).pack(
            anchor="w",
            padx=15,
            pady=10
        )

        marco = tk.Frame(
            self.ventana,
            bg=FONDO
        )

        marco.pack(
            fill="both",
            expand=True,
            padx=15
        )

        self.canvas = tk.Canvas(
            marco,
            bg=LILA_CLARO,
            highlightthickness=0
        )

        barra_h = ttk.Scrollbar(
            marco,
            orient="horizontal",
            command=self.canvas.xview
        )

        barra_v = ttk.Scrollbar(
            marco,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            xscrollcommand=barra_h.set,
            yscrollcommand=barra_v.set
        )

        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        barra_h.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        barra_v.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

        self.estado = tk.Label(
            self.ventana,
            bg=FONDO,
            fg=LILA,
            font=("Segoe UI", 10, "bold")
        )

        self.estado.pack(
            anchor="w",
            padx=15,
            pady=12
        )

    # ======================================
    # VALIDAR ENTRADAS
    # ======================================

    def leer_numero(self, entrada, nombre):

        texto = entrada.get().strip()

        if not texto:
            raise ValueError(
                f"Debes ingresar {nombre}."
            )

        try:
            return int(texto)
        except ValueError:
            raise ValueError(
                f"{nombre.capitalize()} debe ser entero."
            )

    # ======================================
    # INSERTAR USANDO NUESTRA BIBLIOTECA
    # ======================================

    def insertar(self):

        try:
            dato = self.leer_numero(
                self.entrada_dato,
                "el dato"
            )

            modo = self.operacion.get()

            if modo == "Al inicio":

                nodo = self.lista.insertar_inicio(dato)

            elif modo == "Al final":

                nodo = self.lista.insertar_final(dato)

            else:

                posicion = self.leer_numero(
                    self.entrada_posicion,
                    "la posición"
                )

                nodo = self.lista.insertar_posicion(
                    dato,
                    posicion
                )

            self.resaltados = {nodo.id}

            self.registrar(
                "INSERCIÓN",
                f"Nodo ID {nodo.id}, dato {dato}, {modo}"
            )

            self.registrar_extremos()
            self.actualizar_lista()

            self.entrada_dato.delete(0, tk.END)

        except ValueError as error:

            messagebox.showerror(
                "Error al insertar",
                str(error)
            )

    # ======================================
    # BUSCAR USANDO NUESTRA BIBLIOTECA
    # ======================================

    def buscar(self):

        try:
            dato = self.leer_numero(
                self.entrada_dato,
                "el dato"
            )

            resultados = self.lista.buscar(dato)

            self.resaltados = {
                nodo.id
                for posicion, nodo in resultados
            }

            if resultados:

                posiciones = ", ".join(
                    str(posicion)
                    for posicion, nodo in resultados
                )

                self.registrar(
                    "BÚSQUEDA",
                    f"Dato {dato}, posiciones {posiciones}"
                )

                messagebox.showinfo(
                    "Resultado",
                    f"El dato {dato} se encontró "
                    f"en las posiciones: {posiciones}"
                )

            else:

                self.registrar(
                    "BÚSQUEDA",
                    f"Dato {dato} no encontrado"
                )

                messagebox.showinfo(
                    "Resultado",
                    "El dato no se encuentra en la lista."
                )

            self.actualizar_lista()

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ======================================
    # ELIMINAR USANDO NUESTRA BIBLIOTECA
    # ======================================

    def eliminar(self):

        try:
            posicion = self.leer_numero(
                self.entrada_posicion,
                "la posición"
            )

            eliminado = self.lista.eliminar_posicion(
                posicion
            )

            self.resaltados.clear()

            self.registrar(
                "ELIMINACIÓN",
                f"Se eliminó el nodo {eliminado.dato}"
            )

            self.registrar_extremos()
            self.actualizar_lista()

        except ValueError as error:

            messagebox.showerror(
                "Error al eliminar",
                str(error)
            )

    # ======================================
    # CONECTAR USANDO NUESTRA BIBLIOTECA
    # ======================================

    def conectar(self):

        try:
            origen = self.leer_numero(
                self.entrada_origen,
                "el ID de origen"
            )

            destino = self.leer_numero(
                self.entrada_destino,
                "el ID de destino"
            )

            nodo_origen, nodo_destino = (
                self.lista.conectar(origen, destino)
            )

            self.resaltados = {
                nodo_origen.id,
                nodo_destino.id
            }

            self.registrar(
                "CONEXIÓN",
                f"ID {origen} apunta a ID {destino}"
            )

            self.registrar_extremos()
            self.actualizar_lista()

        except ValueError as error:

            messagebox.showerror(
                "Error de conexión",
                str(error)
            )

    # ======================================
    # DESCONECTAR USANDO NUESTRA BIBLIOTECA
    # ======================================

    def desconectar(self):

        try:
            origen = self.leer_numero(
                self.entrada_origen,
                "el ID de origen"
            )

            nodo = self.lista.desconectar(origen)

            self.resaltados = {nodo.id}

            self.registrar(
                "DESCONEXIÓN",
                f"El nodo ID {origen} apunta a None"
            )

            self.registrar_extremos()
            self.actualizar_lista()

        except ValueError as error:

            messagebox.showerror(
                "Error al desconectar",
                str(error)
            )

    # ======================================
    # LIMPIAR USANDO NUESTRA BIBLIOTECA
    # ======================================

    def limpiar(self):

        if not self.lista.nodos:
            messagebox.showinfo(
                "Lista vacía",
                "No hay elementos para eliminar."
            )
            return

        confirmar = messagebox.askyesno(
            "Limpiar lista",
            "¿Deseas eliminar todos los nodos?"
        )

        if confirmar:

            self.lista.limpiar()
            self.resaltados.clear()

            self.registrar(
                "LIMPIEZA",
                "Se eliminaron todos los nodos"
            )

            self.actualizar_lista()

    # ======================================
    # HISTORIAL INDEPENDIENTE
    # ======================================

    def registrar(self, accion, detalle):

        hora = datetime.now().strftime("%H:%M:%S")

        registro = (
            f"[{hora}] {accion}: {detalle}"
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

        nodos = self.lista.recorrido()

        if nodos:

            self.registrar(
                "PRIMERO",
                str(nodos[0].dato)
            )

            self.registrar(
                "ÚLTIMO VISIBLE",
                str(nodos[-1].dato)
            )

        else:

            self.registrar(
                "ESTADO",
                "Lista vacía"
            )

    def abrir_historial(self):

        if (
            self.ventana_historial is not None
            and self.ventana_historial.winfo_exists()
        ):

            self.ventana_historial.lift()
            return

        ventana = tk.Toplevel(self.ventana)

        self.ventana_historial = ventana

        ventana.title(
            "Historial | LinkedList Studio"
        )

        ventana.geometry("820x450")
        ventana.configure(bg=FONDO)

        tk.Label(
            ventana,
            text="Historial de operaciones",
            bg=FONDO,
            fg=LILA,
            font=("Segoe UI", 20, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )

        marco = tk.Frame(
            ventana,
            bg=PANEL
        )

        marco.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )

        self.lista_historial = tk.Listbox(
            marco,
            bg=PANEL,
            fg=TEXTO,
            font=("Consolas", 10),
            selectbackground=MORADO,
            relief="flat"
        )

        self.lista_historial.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra = ttk.Scrollbar(
            marco,
            command=self.lista_historial.yview
        )

        barra.pack(
            side="right",
            fill="y"
        )

        self.lista_historial.configure(
            yscrollcommand=barra.set
        )

        for registro in self.registros:

            self.lista_historial.insert(
                tk.END,
                registro
            )

        acciones = tk.Frame(
            ventana,
            bg=FONDO
        )

        acciones.pack(
            fill="x",
            padx=15,
            pady=12
        )

        self.crear_boton(
            acciones,
            "Borrar historial",
            self.borrar_historial,
            ROJO
        ).pack(side="left")

        self.crear_boton(
            acciones,
            "Cerrar",
            ventana.destroy,
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
            "Historial borrado"
        )

    # ======================================
    # ACTUALIZAR AYUDA
    # ======================================

    def actualizar_ayuda(self):

        total = self.lista.cantidad()

        if self.operacion.get() == "Al inicio":

            texto = "Se insertará al inicio."

        elif self.operacion.get() == "Al final":

            texto = (
                "Se insertará al final "
                "si no existe un ciclo."
            )

        else:

            texto = (
                f"Posiciones disponibles: 1 a {total + 1}"
            )

        self.ayuda.configure(text=texto)

    # ======================================
    # REPRESENTACIÓN VISUAL
    # ======================================

    def actualizar_lista(self):

        self.canvas.delete("all")

        # Consultar nuestra biblioteca
        recorrido = self.lista.recorrido()
        desconectados = self.lista.nodos_desconectados()

        todos = recorrido + desconectados

        if not todos:

            self.canvas.create_text(
                320,
                130,
                text="Lista vacía\nInserta un número",
                fill=MORADO_OSCURO,
                font=("Segoe UI", 17),
                justify="center"
            )

            self.canvas.configure(
                scrollregion=(0, 0, 800, 350)
            )

            self.estado.configure(
                text="Total de nodos: 0"
            )

            self.actualizar_ayuda()
            return

        ancho = 110
        alto = 70
        salto = 190

        posiciones = {}

        grupos = [
            ("RUTA PRINCIPAL", recorrido, 160),
            ("NODOS DESCONECTADOS", desconectados, 360)
        ]

        # DIBUJAR NODOS
        for titulo, nodos, centro_y in grupos:

            if not nodos:
                continue

            self.canvas.create_text(
                25,
                centro_y - 95,
                text=titulo,
                anchor="w",
                fill=MORADO_OSCURO,
                font=("Segoe UI", 11, "bold")
            )

            for i, nodo in enumerate(nodos):

                x = 30 + i * salto
                y = centro_y - alto / 2

                posiciones[nodo.id] = (x, y)

                seleccionado = (
                    nodo.id in self.resaltados
                )

                fondo_nodo = (
                    LILA_SELECCION
                    if seleccionado
                    else LILA_CLARO
                )

                borde = (
                    MORADO
                    if seleccionado
                    else "#A78BFA"
                )

                self.canvas.create_rectangle(
                    x,
                    y,
                    x + ancho,
                    y + alto,
                    fill=fondo_nodo,
                    outline=borde,
                    width=3 if seleccionado else 2
                )

                # SEPARAR DATO Y LIGA
                self.canvas.create_line(
                    x + 74,
                    y,
                    x + 74,
                    y + alto,
                    fill=borde,
                    width=2
                )

                self.canvas.create_text(
                    x + 37,
                    centro_y,
                    text=str(nodo.dato),
                    fill="#4C1D95",
                    font=("Segoe UI", 16, "bold")
                )

                self.canvas.create_text(
                    x + 92,
                    centro_y,
                    text="liga",
                    fill="#6D28D9",
                    font=("Segoe UI", 9)
                )

                self.canvas.create_text(
                    x + ancho / 2,
                    y - 20,
                    text=f"ID {nodo.id}",
                    fill="#4C1D95",
                    font=("Segoe UI", 10, "bold")
                )

        # DIBUJAR CONEXIONES
        for nodo in todos:

            x, y = posiciones[nodo.id]

            if nodo.liga is None:

                self.canvas.create_line(
                    x + ancho,
                    y + alto / 2,
                    x + ancho + 30,
                    y + alto / 2,
                    fill=MORADO,
                    width=2,
                    arrow=tk.LAST
                )

                self.canvas.create_text(
                    x + ancho + 35,
                    y + alto / 2,
                    text="None",
                    anchor="w",
                    fill=MORADO_OSCURO
                )

                continue

            if nodo.liga.id not in posiciones:
                continue

            dx, dy = posiciones[nodo.liga.id]

            # CONEXIÓN DIRECTA
            if (
                abs(dx - x - salto) < 1
                and abs(dy - y) < 1
            ):

                self.canvas.create_line(
                    x + ancho,
                    y + alto / 2,
                    dx,
                    dy + alto / 2,
                    fill=MORADO,
                    width=3,
                    arrow=tk.LAST
                )

            # CONEXIÓN MODIFICADA
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

        # ACTUALIZAR TAMAÑO DEL CANVAS
        ancho_total = max(
            850,
            220 + max(
                len(recorrido),
                len(desconectados)
            ) * salto
        )

        alto_total = (
            510 if desconectados else 300
        )

        self.canvas.configure(
            scrollregion=(
                0,
                0,
                ancho_total,
                alto_total
            )
        )

        # ESTADO ACTUAL
        primero = (
            recorrido[0].dato
            if recorrido else "—"
        )

        ultimo = (
            recorrido[-1].dato
            if recorrido else "—"
        )

        ciclo = (
            "Sí"
            if self.lista.hay_ciclo()
            else "No"
        )

        self.estado.configure(
            text=(
                f"Total: {len(todos)} nodos"
                f"  |  Alcanzables: {len(recorrido)}"
                f"  |  Desconectados: {len(desconectados)}"
                f"  |  Primero: {primero}"
                f"  |  Último visible: {ultimo}"
                f"  |  Ciclo: {ciclo}"
            )
        )

        self.actualizar_ayuda()


# ==========================================
# EJECUCIÓN
# ==========================================

if __name__ == "__main__":

    ventana = tk.Tk()

    aplicacion = Aplicacion(ventana)

    ventana.mainloop()
