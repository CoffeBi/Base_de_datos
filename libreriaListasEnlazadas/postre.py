
import tkinter as tk
import json
from pathlib import Path
from tkinter import ttk, messagebox, filedialog

# ==================================================
# CONFIGURACIÓN GENERAL
# ==================================================

ARCHIVO = Path(__file__).with_name("postres_datos.json")

COLORES = {
    "fondo": "#F8F4FC",
    "blanco": "#FFFFFF",
    "lavanda": "#EDE4F8",
    "morado": "#7960A6",
    "claro": "#B8A0DF",
    "texto": "#46375B",
    "secundario": "#80728F",
    "borde": "#E4D8F0"
}


def normalizar(texto):
    return texto.strip().casefold()


# ==================================================
# LISTA ENLAZADA DE INGREDIENTES
# ==================================================

class NodoIngrediente:

    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


class ListaIngredientes:

    def __init__(self, valores=None):
        self.cabeza = None
        self.cola = None

        if valores is not None:
            for valor in valores:
                self.agregar(valor)

    def __iter__(self):
        actual = self.cabeza

        while actual is not None:
            yield actual.valor
            actual = actual.siguiente

    def __len__(self):
        return sum(1 for _ in self)

    def existe(self, valor):
        return any(
            normalizar(i) == normalizar(valor)
            for i in self
        )

    def agregar(self, valor):
        valor = valor.strip()

        if not valor or self.existe(valor):
            return False

        nuevo = NodoIngrediente(valor)

        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            self.cola.siguiente = nuevo

        self.cola = nuevo
        return True

    def eliminar(self, valor):
        anterior = None
        actual = self.cabeza

        while actual is not None:
            if normalizar(actual.valor) == normalizar(valor):

                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                if self.cola is actual:
                    self.cola = anterior

                return True

            anterior = actual
            actual = actual.siguiente

        return False

    def convertir_lista(self):
        return list(self)


# ==================================================
# ESTRUCTURA DE POSTRE
# ==================================================

class Postre:

    def __init__(self, nombre, ingredientes=None, pasos=None):
        self.nombre = nombre.strip()
        self.ingredientes = ListaIngredientes(ingredientes)
        self.pasos = list(pasos or [])

    def convertir_diccionario(self):
        return {
            "nombre": self.nombre,
            "ingredientes": self.ingredientes.convertir_lista(),
            "pasos": self.pasos.copy()
        }


# Arreglo principal vacío
POSTRES = []


# ==================================================
# FUNCIONES GENERALES
# ==================================================

def ordenar_postres():
    POSTRES.sort(key=lambda p: normalizar(p.nombre))


def buscar_postre(nombre):
    for postre in POSTRES:
        if normalizar(postre.nombre) == normalizar(nombre):
            return postre
    return None


def limpiar_ingredientes(texto):
    lista = ListaIngredientes()

    for linea in texto.splitlines():
        lista.agregar(linea)

    return lista.convertir_lista()


def limpiar_pasos(texto):
    return [
        linea.strip()
        for linea in texto.splitlines()
        if linea.strip()
    ]


# ==================================================
# EJERCICIO 2 - ELIMINAR REGISTROS REPETIDOS
# ==================================================

def fusionar_repetidos(arreglo):
    resultado = []
    encontrados = {}

    postres_repetidos = 0
    ingredientes_repetidos = 0
    pasos_repetidos = 0

    for postre in arreglo:
        clave = normalizar(postre.nombre)

        if clave not in encontrados:
            nuevo = Postre(postre.nombre)
            encontrados[clave] = nuevo
            resultado.append(nuevo)
        else:
            postres_repetidos += 1

        destino = encontrados[clave]

        for ingrediente in postre.ingredientes:
            if not destino.ingredientes.agregar(ingrediente):
                ingredientes_repetidos += 1

        vistos = {normalizar(p) for p in destino.pasos}

        for paso in postre.pasos:
            if normalizar(paso) not in vistos:
                destino.pasos.append(paso)
                vistos.add(normalizar(paso))
            else:
                pasos_repetidos += 1

    resultado.sort(key=lambda p: normalizar(p.nombre))

    return resultado, (
        postres_repetidos,
        ingredientes_repetidos,
        pasos_repetidos
    )


# ==================================================
# VALIDAR ARCHIVOS JSON
# ==================================================

def validar_json(datos):

    if not isinstance(datos, list):
        raise ValueError("El archivo debe contener una lista.")

    resultado = []

    for numero, registro in enumerate(datos, 1):

        if not isinstance(registro, dict):
            raise ValueError(f"Registro {numero} inválido.")

        nombre = registro.get("nombre")
        ingredientes = registro.get("ingredientes")
        pasos = registro.get("pasos", [])

        if (
            not isinstance(nombre, str)
            or not nombre.strip()
            or nombre.strip() == "0"
        ):
            raise ValueError(f"Nombre inválido en registro {numero}.")

        if (
            not isinstance(ingredientes, list)
            or not ingredientes
            or not all(
                isinstance(i, str) and i.strip()
                for i in ingredientes
            )
        ):
            raise ValueError(
                f"Ingredientes inválidos en registro {numero}."
            )

        if (
            not isinstance(pasos, list)
            or not all(
                isinstance(p, str) and p.strip()
                for p in pasos
            )
        ):
            raise ValueError(
                f"Procedimiento inválido en registro {numero}."
            )

        resultado.append(Postre(nombre, ingredientes, pasos))

    return resultado


# ==================================================
# APLICACIÓN GRÁFICA
# ==================================================

class SistemaPostres(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Sistema de Postres - Lavanda")
        self.geometry("1100x740")
        self.minsize(900, 600)
        self.configure(bg=COLORES["fondo"])

        self.busqueda = tk.StringVar()
        self.seleccion_actual = None

        self.configurar_estilos()
        self.crear_interfaz()
        self.cargar_datos()
        self.actualizar_tabla()

        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    # ======================================
    # CONFIGURACIÓN DE ESTILOS
    # ======================================

    def configurar_estilos(self):

        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure(
            "Postres.Treeview",
            background="white",
            fieldbackground="white",
            foreground=COLORES["texto"],
            rowheight=35,
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "Postres.Treeview.Heading",
            background=COLORES["lavanda"],
            foreground=COLORES["texto"],
            font=("Segoe UI", 10, "bold"),
            padding=10
        )

        estilo.map(
            "Postres.Treeview",
            background=[("selected", COLORES["claro"])],
            foreground=[("selected", COLORES["texto"])]
        )

    # ======================================
    # CREAR BOTONES
    # ======================================

    def boton(self, padre, texto, comando, principal=False):

        return tk.Button(
            padre,
            text=texto,
            command=comando,
            bg=COLORES["morado"] if principal else COLORES["lavanda"],
            fg="white" if principal else COLORES["texto"],
            activebackground=COLORES["claro"],
            activeforeground=COLORES["texto"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=9
        )

    # ======================================
    # CREAR VENTANAS
    # ======================================

    def crear_ventana(self, titulo, ancho=700, alto=570):

        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry(f"{ancho}x{alto}")
        ventana.minsize(580, 490)
        ventana.configure(bg=COLORES["fondo"])
        ventana.transient(self)

        return ventana

    # ======================================
    # INTERFAZ PRINCIPAL
    # ======================================

    def crear_interfaz(self):

        cabecera = tk.Frame(self, bg=COLORES["fondo"])
        cabecera.pack(fill="x", padx=24, pady=(18, 10))

        tk.Label(
            cabecera,
            text="Sistema de Postres",
            bg=COLORES["fondo"],
            fg=COLORES["morado"],
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")

        tk.Label(
            cabecera,
            text="Administra postres, ingredientes y procedimientos",
            bg=COLORES["fondo"],
            fg=COLORES["secundario"],
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        cuerpo = tk.Frame(self, bg=COLORES["fondo"])
        cuerpo.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 10)
        )

        # MENÚ LATERAL

        lateral = tk.Frame(
            cuerpo,
            bg=COLORES["lavanda"],
            width=240,
            padx=10,
            pady=12
        )

        lateral.pack(side="left", fill="y", padx=(0, 14))
        lateral.pack_propagate(False)

        tk.Label(
            lateral,
            text="OPERACIONES",
            bg=COLORES["lavanda"],
            fg=COLORES["morado"],
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(0, 10))

        acciones = [
            ("Registrar postre", self.registrar),
            ("Ver receta completa", self.ver_receta),
            ("Editar receta", self.editar),
            ("Agregar ingredientes", self.agregar_ingredientes),
            ("Eliminar ingredientes", self.eliminar_ingredientes),
            ("Agregar pasos", self.agregar_pasos),
            ("Eliminar postre", self.eliminar_postre),
            ("Eliminar repetidos", self.eliminar_repetidos),
            ("Probar duplicados", self.probar_duplicados),
            ("Exportar JSON", self.exportar),
            ("Importar JSON", self.importar)
        ]

        for indice, (texto, funcion) in enumerate(acciones):
            self.boton(
                lateral,
                texto,
                funcion,
                indice == 0
            ).pack(fill="x", pady=2)

        # PANEL PRINCIPAL

        panel = tk.Frame(
            cuerpo,
            bg="white",
            padx=17,
            pady=16,
            highlightthickness=1,
            highlightbackground=COLORES["borde"]
        )
        panel.pack(side="left", fill="both", expand=True)

        encabezado = tk.Frame(panel, bg="white")
        encabezado.pack(fill="x")

        tk.Label(
            encabezado,
            text="Mis postres",
            bg="white",
            fg=COLORES["texto"],
            font=("Segoe UI", 17, "bold")
        ).pack(side="left")

        self.contador = tk.Label(
            encabezado,
            bg="white",
            fg=COLORES["secundario"],
            font=("Segoe UI", 10)
        )
        self.contador.pack(side="right")

        tk.Label(
            panel,
            text="Buscar por nombre",
            bg="white",
            fg=COLORES["secundario"],
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(12, 4))

        tk.Entry(
            panel,
            textvariable=self.busqueda,
            bg=COLORES["fondo"],
            fg=COLORES["texto"],
            font=("Segoe UI", 11),
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORES["borde"]
        ).pack(fill="x", ipady=8, pady=(0, 10))

        self.busqueda.trace_add(
            "write",
            lambda *_: self.actualizar_tabla()
        )

        # TABLA

        marco = tk.Frame(panel, bg="white")
        marco.pack(fill="both", expand=True)

        self.tabla = ttk.Treeview(
            marco,
            columns=("nombre", "ingredientes", "pasos"),
            show="headings",
            selectmode="browse",
            style="Postres.Treeview"
        )

        columnas = [
            ("nombre", "Nombre del postre", 260),
            ("ingredientes", "Ingredientes", 110),
            ("pasos", "Pasos", 70)
        ]

        for columna, titulo, ancho in columnas:

            self.tabla.heading(columna, text=titulo)
            self.tabla.column(
                columna,
                width=ancho,
                anchor="w" if columna == "nombre" else "center"
            )

        self.tabla.pack(side="left", fill="both", expand=True)

        barra = ttk.Scrollbar(
            marco,
            orient="vertical",
            command=self.tabla.yview
        )
        barra.pack(side="right", fill="y")

        self.tabla.configure(yscrollcommand=barra.set)

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.mostrar_detalle
        )

        self.tabla.bind(
            "<Double-1>",
            lambda _: self.ver_receta()
        )

        tk.Label(
            panel,
            text="Vista rápida",
            bg="white",
            fg=COLORES["texto"],
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(12, 6))

        self.detalle = tk.Label(
            panel,
            text="Selecciona un postre.",
            bg=COLORES["lavanda"],
            fg=COLORES["texto"],
            anchor="nw",
            justify="left",
            wraplength=570,
            padx=12,
            pady=10,
            font=("Segoe UI", 10)
        )
        self.detalle.pack(fill="x")

        self.estado = tk.Label(
            self,
            text="Sistema listo",
            bg=COLORES["fondo"],
            fg=COLORES["secundario"],
            anchor="w",
            font=("Segoe UI", 9)
        )
        self.estado.pack(fill="x", padx=24, pady=(0, 7))

    # ======================================
    # SELECCIONAR POSTRE
    # ======================================

    def seleccionado(self, avisar=True):

        ids = self.tabla.selection()

        if ids:
            try:
                indice = int(ids[0])

                if 0 <= indice < len(POSTRES):
                    return POSTRES[indice]

            except ValueError:
                pass

        if avisar:
            messagebox.showinfo(
                "Seleccionar postre",
                "Selecciona un postre en la tabla.",
                parent=self
            )

        return None

    # ======================================
    # ACTUALIZAR TABLA
    # ======================================

    def actualizar_tabla(self, seleccionar=None):

        objetivo = (
            seleccionar
            if seleccionar is not None
            else self.seleccion_actual
        )

        ordenar_postres()
        self.tabla.delete(*self.tabla.get_children())

        filtro = normalizar(self.busqueda.get())

        for indice, postre in enumerate(POSTRES):

            if filtro in normalizar(postre.nombre):

                identificador = str(indice)

                self.tabla.insert(
                    "",
                    "end",
                    iid=identificador,
                    values=(
                        postre.nombre,
                        len(postre.ingredientes),
                        len(postre.pasos)
                    )
                )

                if postre is objetivo:
                    self.tabla.selection_set(identificador)
                    self.tabla.see(identificador)

        self.contador.config(
            text=f"{len(POSTRES)} registrados"
        )

        self.mostrar_detalle()

    # ======================================
    # MOSTRAR DETALLES
    # ======================================

    def mostrar_detalle(self, evento=None):

        postre = self.seleccionado(False)
        self.seleccion_actual = postre

        if postre is None:
            self.detalle.config(
                text="Selecciona un postre para consultar su receta."
            )
            return

        ingredientes = ", ".join(
            postre.ingredientes
        ) or "Sin ingredientes"

        self.detalle.config(
            text=(
                f"{postre.nombre}\n"
                f"Ingredientes: {ingredientes}\n"
                f"Pasos de preparación: {len(postre.pasos)}"
            )
        )

    # ======================================
    # FORMULARIO CON BOTONES FIJOS
    # ======================================

    def formulario(self, titulo, postre=None, modo="completo"):

        ventana = self.crear_ventana(
            titulo,
            760,
            560
        )
        ventana.minsize(650, 500)

        resultado = {"datos": None}

        principal = tk.Frame(
            ventana,
            bg=COLORES["fondo"]
        )
        principal.pack(fill="both", expand=True)

        # Reservar primero el espacio de los botones
        barra_inferior = tk.Frame(
            principal,
            bg=COLORES["lavanda"],
            height=78,
            padx=20,
            pady=12
        )
        barra_inferior.pack(side="bottom", fill="x")
        barra_inferior.pack_propagate(False)

        contenido = tk.Frame(
            principal,
            bg=COLORES["fondo"],
            padx=24,
            pady=18
        )
        contenido.pack(side="top", fill="both", expand=True)

        tk.Label(
            contenido,
            text=titulo,
            bg=COLORES["fondo"],
            fg=COLORES["morado"],
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w")

        tk.Label(
            contenido,
            text="Completa los campos y guarda los cambios.",
            bg=COLORES["fondo"],
            fg=COLORES["secundario"],
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 12))

        tk.Label(
            contenido,
            text="Nombre del postre",
            bg=COLORES["fondo"],
            fg=COLORES["texto"],
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        entrada_nombre = tk.Entry(
            contenido,
            font=("Segoe UI", 11),
            bg="white",
            fg=COLORES["texto"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORES["borde"]
        )
        entrada_nombre.pack(
            fill="x",
            ipady=8,
            pady=(5, 14)
        )

        if postre:
            entrada_nombre.insert(0, postre.nombre)

        if modo != "completo":
            entrada_nombre.config(state="disabled")

        columnas = tk.Frame(
            contenido,
            bg=COLORES["fondo"]
        )
        columnas.pack(fill="both", expand=True)

        columnas.grid_columnconfigure(0, weight=1)
        columnas.grid_columnconfigure(1, weight=1)
        columnas.grid_rowconfigure(1, weight=1)

        tk.Label(
            columnas,
            text="Ingredientes (uno por línea)",
            bg=COLORES["fondo"],
            fg=COLORES["texto"],
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 6)
        )

        tk.Label(
            columnas,
            text="Procedimiento (un paso por línea)",
            bg=COLORES["fondo"],
            fg=COLORES["texto"],
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(10, 0),
            pady=(0, 6)
        )

        area_ingredientes = tk.Text(
            columnas,
            wrap="word",
            font=("Segoe UI", 10),
            bg="white",
            fg=COLORES["texto"],
            relief="flat",
            padx=10,
            pady=10,
            height=8,
            highlightthickness=1,
            highlightbackground=COLORES["borde"]
        )
        area_ingredientes.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        area_pasos = tk.Text(
            columnas,
            wrap="word",
            font=("Segoe UI", 10),
            bg="white",
            fg=COLORES["texto"],
            relief="flat",
            padx=10,
            pady=10,
            height=8,
            highlightthickness=1,
            highlightbackground=COLORES["borde"]
        )
        area_pasos.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        # Cargar datos al editar
        if postre and modo == "completo":
            area_ingredientes.insert(
                "1.0",
                "\n".join(postre.ingredientes)
            )

            area_pasos.insert(
                "1.0",
                "\n".join(postre.pasos)
            )

        if modo == "ingredientes":
            area_pasos.config(state="disabled")

        elif modo == "pasos":
            area_ingredientes.config(state="disabled")

        # Contador
        contador = tk.Label(
            contenido,
            text="0 ingredientes · 0 pasos",
            bg=COLORES["fondo"],
            fg=COLORES["secundario"],
            font=("Segoe UI", 9)
        )
        contador.pack(anchor="e", pady=(6, 0))

        def actualizar_contador(evento=None):

            ingredientes = [
                x for x in area_ingredientes.get(
                    "1.0", "end-1c"
                ).splitlines()
                if x.strip()
            ]

            pasos = [
                x for x in area_pasos.get(
                    "1.0", "end-1c"
                ).splitlines()
                if x.strip()
            ]

            contador.config(
                text=(
                    f"{len(ingredientes)} ingredientes · "
                    f"{len(pasos)} pasos"
                )
            )

        area_ingredientes.bind(
            "<KeyRelease>",
            actualizar_contador
        )
        area_pasos.bind(
            "<KeyRelease>",
            actualizar_contador
        )

        actualizar_contador()

        # GUARDAR DATOS
        def guardar():

            nombre = entrada_nombre.get().strip()

            if not nombre or nombre == "0":
                messagebox.showwarning(
                    "Nombre inválido",
                    "Ingresa un nombre válido.",
                    parent=ventana
                )
                return

            if modo == "completo":
                existente = buscar_postre(nombre)

                if existente is not None and existente is not postre:
                    messagebox.showwarning(
                        "Postre repetido",
                        "Ya existe un postre con ese nombre.",
                        parent=ventana
                    )
                    return

            ingredientes = []
            pasos = []

            if modo != "pasos":
                ingredientes = limpiar_ingredientes(
                    area_ingredientes.get("1.0", "end-1c")
                )

            if modo != "ingredientes":
                pasos = limpiar_pasos(
                    area_pasos.get("1.0", "end-1c")
                )

            if modo in ("completo", "ingredientes") and not ingredientes:
                messagebox.showwarning(
                    "Ingredientes requeridos",
                    "Ingresa al menos un ingrediente.",
                    parent=ventana
                )
                return

            if modo == "pasos" and not pasos:
                messagebox.showwarning(
                    "Procedimiento requerido",
                    "Ingresa al menos un paso.",
                    parent=ventana
                )
                return

            resultado["datos"] = {
                "nombre": nombre,
                "ingredientes": ingredientes,
                "pasos": pasos
            }

            ventana.destroy()

        # BOTONES INFERIORES FIJOS

        self.boton(
            barra_inferior,
            "Cancelar",
            ventana.destroy
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8)
        )

        self.boton(
            barra_inferior,
            "Guardar cambios",
            guardar,
            True
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(8, 0)
        )

        ventana.grab_set()

        if modo == "completo":
            entrada_nombre.focus_set()
        elif modo == "ingredientes":
            area_ingredientes.focus_set()
        else:
            area_pasos.focus_set()

        self.wait_window(ventana)

        return resultado["datos"]

    # ======================================
    # REGISTRAR NUEVO POSTRE
    # ======================================

    def registrar(self):

        datos = self.formulario("Registrar nuevo postre")

        if datos is None:
            return

        postre = Postre(**datos)
        POSTRES.append(postre)

        self.busqueda.set("")
        self.actualizar_tabla(postre)
        self.guardar_datos()

        messagebox.showinfo(
            "Registro exitoso",
            "Postre registrado correctamente.",
            parent=self
        )

    # ======================================
    # EDITAR RECETA
    # ======================================

    def editar(self):

        postre = self.seleccionado()

        if postre is None:
            return

        datos = self.formulario("Editar receta", postre)

        if datos is None:
            return

        postre.nombre = datos["nombre"]
        postre.ingredientes = ListaIngredientes(
            datos["ingredientes"]
        )
        postre.pasos = datos["pasos"]

        self.busqueda.set("")
        self.actualizar_tabla(postre)
        self.guardar_datos()

        messagebox.showinfo(
            "Receta actualizada",
            "Los cambios fueron guardados.",
            parent=self
        )

    # ======================================
    # AGREGAR INGREDIENTES
    # ======================================

    def agregar_ingredientes(self):

        postre = self.seleccionado()

        if postre is None:
            return

        datos = self.formulario(
            "Agregar ingredientes",
            postre,
            "ingredientes"
        )

        if datos is None:
            return

        agregados = 0

        for ingrediente in datos["ingredientes"]:
            if postre.ingredientes.agregar(ingrediente):
                agregados += 1

        self.actualizar_tabla(postre)
        self.guardar_datos()

        messagebox.showinfo(
            "Ingredientes",
            f"Se agregaron {agregados} ingredientes nuevos.",
            parent=self
        )

    # ======================================
    # ELIMINAR INGREDIENTES
    # ======================================

    def eliminar_ingredientes(self):

        postre = self.seleccionado()

        if postre is None:
            return

        ingredientes = postre.ingredientes.convertir_lista()

        if not ingredientes:
            messagebox.showinfo(
                "Sin ingredientes",
                "Este postre no tiene ingredientes.",
                parent=self
            )
            return

        ventana = self.crear_ventana(
            "Eliminar ingredientes",
            470,
            410
        )

        principal = tk.Frame(
            ventana,
            bg=COLORES["fondo"]
        )
        principal.pack(fill="both", expand=True)

        barra_inferior = tk.Frame(
            principal,
            bg=COLORES["lavanda"],
            height=75,
            padx=15,
            pady=12
        )
        barra_inferior.pack(side="bottom", fill="x")
        barra_inferior.pack_propagate(False)

        panel = tk.Frame(
            principal,
            bg=COLORES["fondo"],
            padx=20,
            pady=18
        )
        panel.pack(fill="both", expand=True)

        tk.Label(
            panel,
            text="Eliminar ingredientes",
            bg=COLORES["fondo"],
            fg=COLORES["morado"],
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", pady=(0, 12))

        lista = tk.Listbox(
            panel,
            selectmode="extended",
            font=("Segoe UI", 11),
            bg="white",
            fg=COLORES["texto"],
            selectbackground=COLORES["claro"],
            relief="flat"
        )
        lista.pack(fill="both", expand=True)

        for ingrediente in ingredientes:
            lista.insert("end", ingrediente)

        def eliminar():

            indices = lista.curselection()

            if not indices:
                messagebox.showwarning(
                    "Sin selección",
                    "Selecciona al menos un ingrediente.",
                    parent=ventana
                )
                return

            if len(indices) == len(ingredientes):
                messagebox.showwarning(
                    "Operación no permitida",
                    "El postre debe conservar al menos un ingrediente.",
                    parent=ventana
                )
                return

            for indice in indices:
                postre.ingredientes.eliminar(
                    ingredientes[indice]
                )

            ventana.destroy()
            self.actualizar_tabla(postre)
            self.guardar_datos()

        self.boton(
            barra_inferior,
            "Cancelar",
            ventana.destroy
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.boton(
            barra_inferior,
            "Eliminar seleccionados",
            eliminar,
            True
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

        ventana.grab_set()

    # ======================================
    # AGREGAR PASOS DE PREPARACIÓN
    # ======================================

    def agregar_pasos(self):

        postre = self.seleccionado()

        if postre is None:
            return

        datos = self.formulario(
            "Agregar pasos de preparación",
            postre,
            "pasos"
        )

        if datos is None:
            return

        postre.pasos.extend(datos["pasos"])

        self.actualizar_tabla(postre)
        self.guardar_datos()

        messagebox.showinfo(
            "Procedimiento",
            f"Se agregaron {len(datos['pasos'])} pasos.",
            parent=self
        )

    # ==================================================
    # VER RECETA COMPLETA - DISEÑO MEJORADO
    # ==================================================

    def ver_receta(self):

        postre = self.seleccionado()

        if postre is None:
            return

        ventana = self.crear_ventana(
            "Receta completa",
            800,
            580
        )

        ventana.minsize(700, 500)

        # CONTENEDOR PRINCIPAL

        principal = tk.Frame(
            ventana,
            bg=COLORES["fondo"]
        )
        principal.pack(fill="both", expand=True)

        # BARRA INFERIOR FIJA

        pie = tk.Frame(
            principal,
            bg=COLORES["lavanda"],
            height=76,
            padx=22,
            pady=12
        )
        pie.pack(side="bottom", fill="x")
        pie.pack_propagate(False)

        self.boton(
            pie,
            "Cerrar receta",
            ventana.destroy,
            True
        ).pack(fill="x")

        # CONTENIDO

        contenedor = tk.Frame(
            principal,
            bg=COLORES["fondo"],
            padx=22,
            pady=18
        )
        contenedor.pack(
            side="top",
            fill="both",
            expand=True
        )

        # ENCABEZADO

        encabezado = tk.Frame(
            contenedor,
            bg=COLORES["fondo"]
        )
        encabezado.pack(fill="x", pady=(0, 15))

        tk.Label(
            encabezado,
            text=postre.nombre,
            bg=COLORES["fondo"],
            fg=COLORES["morado"],
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")

        tk.Label(
            encabezado,
            text=(
                f"{len(postre.ingredientes)} ingredientes"
                f"   •   {len(postre.pasos)} pasos de preparación"
            ),
            bg=COLORES["fondo"],
            fg=COLORES["secundario"],
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(5, 0))

        # CONTENEDOR DE TARJETAS

        tarjetas = tk.Frame(
            contenedor,
            bg=COLORES["fondo"]
        )
        tarjetas.pack(
            fill="both",
            expand=True
        )

        tarjetas.grid_columnconfigure(0, weight=1)
        tarjetas.grid_columnconfigure(1, weight=1)
        tarjetas.grid_rowconfigure(0, weight=1)

        # ======================================
        # TARJETA DE INGREDIENTES
        # ======================================

        tarjeta_ingredientes = tk.Frame(
            tarjetas,
            bg=COLORES["blanco"],
            highlightbackground=COLORES["borde"],
            highlightthickness=1
        )
        tarjeta_ingredientes.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        cabecera_ingredientes = tk.Frame(
            tarjeta_ingredientes,
            bg=COLORES["lavanda"],
            padx=14,
            pady=10
        )
        cabecera_ingredientes.pack(fill="x")

        tk.Label(
            cabecera_ingredientes,
            text="INGREDIENTES",
            bg=COLORES["lavanda"],
            fg=COLORES["texto"],
            font=("Segoe UI", 11, "bold")
        ).pack(side="left")

        tk.Label(
            cabecera_ingredientes,
            text=str(len(postre.ingredientes)),
            bg=COLORES["morado"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=3
        ).pack(side="right")

        cuerpo_ingredientes = tk.Frame(
            tarjeta_ingredientes,
            bg="white",
            padx=10,
            pady=10
        )
        cuerpo_ingredientes.pack(
            fill="both",
            expand=True
        )

        texto_ingredientes = tk.Text(
            cuerpo_ingredientes,
            wrap="word",
            font=("Segoe UI", 11),
            bg="white",
            fg=COLORES["texto"],
            relief="flat",
            padx=8,
            pady=8,
            cursor="arrow"
        )
        texto_ingredientes.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_ingredientes = ttk.Scrollbar(
            cuerpo_ingredientes,
            orient="vertical",
            command=texto_ingredientes.yview
        )
        scroll_ingredientes.pack(
            side="right",
            fill="y"
        )

        texto_ingredientes.configure(
            yscrollcommand=scroll_ingredientes.set
        )

        if len(postre.ingredientes) > 0:
            ingredientes = "\n\n".join(
                f"• {ingrediente}"
                for ingrediente in postre.ingredientes
            )
        else:
            ingredientes = "No hay ingredientes registrados."

        texto_ingredientes.insert(
            "1.0",
            ingredientes
        )
        texto_ingredientes.config(state="disabled")

        # ======================================
        # TARJETA DE PROCEDIMIENTO
        # ======================================

        tarjeta_pasos = tk.Frame(
            tarjetas,
            bg=COLORES["blanco"],
            highlightbackground=COLORES["borde"],
            highlightthickness=1
        )
        tarjeta_pasos.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        cabecera_pasos = tk.Frame(
            tarjeta_pasos,
            bg=COLORES["lavanda"],
            padx=14,
            pady=10
        )
        cabecera_pasos.pack(fill="x")

        tk.Label(
            cabecera_pasos,
            text="PROCEDIMIENTO",
            bg=COLORES["lavanda"],
            fg=COLORES["texto"],
            font=("Segoe UI", 11, "bold")
        ).pack(side="left")

        tk.Label(
            cabecera_pasos,
            text=str(len(postre.pasos)),
            bg=COLORES["morado"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=3
        ).pack(side="right")

        cuerpo_pasos = tk.Frame(
            tarjeta_pasos,
            bg="white",
            padx=10,
            pady=10
        )
        cuerpo_pasos.pack(
            fill="both",
            expand=True
        )

        texto_pasos = tk.Text(
            cuerpo_pasos,
            wrap="word",
            font=("Segoe UI", 11),
            bg="white",
            fg=COLORES["texto"],
            relief="flat",
            padx=8,
            pady=8,
            cursor="arrow"
        )
        texto_pasos.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_pasos = ttk.Scrollbar(
            cuerpo_pasos,
            orient="vertical",
            command=texto_pasos.yview
        )
        scroll_pasos.pack(
            side="right",
            fill="y"
        )

        texto_pasos.configure(
            yscrollcommand=scroll_pasos.set
        )

        if postre.pasos:
            procedimiento = "\n\n".join(
                f"{numero}. {paso}"
                for numero, paso in enumerate(postre.pasos, 1)
            )
        else:
            procedimiento = "No hay pasos registrados."

        texto_pasos.insert(
            "1.0",
            procedimiento
        )
        texto_pasos.config(state="disabled")

        ventana.grab_set()

    # ======================================
    # ELIMINAR POSTRE
    # ======================================

    def eliminar_postre(self):

        postre = self.seleccionado()

        if postre is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar '{postre.nombre}' junto con sus "
            "ingredientes y pasos?",
            parent=self
        )

        if not confirmar:
            return

        POSTRES.remove(postre)
        self.seleccion_actual = None
        self.actualizar_tabla()
        self.guardar_datos()

    # ======================================
    # EJERCICIO 2 - ELIMINAR REPETIDOS
    # ======================================

    def eliminar_repetidos(self):

        if not POSTRES:
            messagebox.showinfo(
                "Sin registros",
                "No hay postres registrados.",
                parent=self
            )
            return

        resultado, cantidades = fusionar_repetidos(POSTRES)

        POSTRES[:] = resultado
        self.seleccion_actual = None

        self.actualizar_tabla()
        self.guardar_datos()

        messagebox.showinfo(
            "Ejercicio 2",
            f"Postres repetidos: {cantidades[0]}\n"
            f"Ingredientes repetidos: {cantidades[1]}\n"
            f"Pasos repetidos: {cantidades[2]}\n"
            f"Postres restantes: {len(POSTRES)}\n\n"
            "Se conservaron los ingredientes y pasos únicos.",
            parent=self
        )

    # ======================================
    # PROBAR DUPLICADOS
    # ======================================

    def probar_duplicados(self):

        if not POSTRES:
            messagebox.showinfo(
                "Sin registros",
                "Registra al menos un postre para probar.",
                parent=self
            )
            return

        pruebas = [
            Postre(
                p.nombre,
                p.ingredientes,
                p.pasos
            )
            for p in POSTRES
        ]

        original = POSTRES[0]

        copia = Postre(
            original.nombre,
            original.ingredientes,
            original.pasos
        )

        pruebas.append(copia)

        cantidad_antes = len(pruebas)

        resultado, cantidades = fusionar_repetidos(pruebas)

        messagebox.showinfo(
            "Prueba del ejercicio 2",
            "PRUEBA TEMPORAL\n\n"
            f"Registros antes: {cantidad_antes}\n"
            f"Registros después: {len(resultado)}\n"
            f"Postres duplicados: {cantidades[0]}\n"
            f"Ingredientes repetidos: {cantidades[1]}\n"
            f"Pasos repetidos: {cantidades[2]}\n\n"
            "Las listas enlazadas se combinaron "
            "sin perder ingredientes únicos.\n\n"
            "Los datos originales no fueron modificados.",
            parent=self
        )

    # ======================================
    # GUARDAR DATOS AUTOMÁTICAMENTE
    # ======================================

    def guardar_datos(self):

        try:
            datos = [
                postre.convertir_diccionario()
                for postre in POSTRES
            ]

            with open(
                ARCHIVO,
                "w",
                encoding="utf-8"
            ) as archivo:
                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=2
                )

            self.estado.config(
                text=f"Datos guardados en {ARCHIVO.name}"
            )

            return True

        except OSError as error:
            messagebox.showerror(
                "Error al guardar",
                str(error),
                parent=self
            )
            return False

    # ======================================
    # CARGAR DATOS
    # ======================================

    def cargar_datos(self):

        if not ARCHIVO.exists():
            return

        try:
            with open(
                ARCHIVO,
                encoding="utf-8"
            ) as archivo:
                datos = json.load(archivo)

            POSTRES[:] = validar_json(datos)

        except (OSError, ValueError) as error:
            messagebox.showwarning(
                "Error al cargar",
                str(error),
                parent=self
            )

    # ======================================
    # EXPORTAR JSON
    # ======================================

    def exportar(self):

        ruta = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json")],
            initialfile="respaldo_postres.json"
        )

        if not ruta:
            return

        try:
            datos = [
                postre.convertir_diccionario()
                for postre in POSTRES
            ]

            with open(
                ruta,
                "w",
                encoding="utf-8"
            ) as archivo:
                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=2
                )

            messagebox.showinfo(
                "Exportación",
                "Respaldo guardado correctamente.",
                parent=self
            )

        except OSError as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self
            )

    # ======================================
    # IMPORTAR JSON
    # ======================================

    def importar(self):

        ruta = filedialog.askopenfilename(
            parent=self,
            filetypes=[("Archivos JSON", "*.json")]
        )

        if not ruta:
            return

        try:
            with open(
                ruta,
                encoding="utf-8"
            ) as archivo:
                datos = validar_json(json.load(archivo))

        except (OSError, ValueError) as error:
            messagebox.showerror(
                "Archivo inválido",
                str(error),
                parent=self
            )
            return

        confirmar = messagebox.askyesno(
            "Importar datos",
            "¿Reemplazar los postres actuales?\n\n"
            "Los registros duplicados se conservarán "
            "para poder probar el ejercicio 2.",
            parent=self
        )

        if not confirmar:
            return

        POSTRES[:] = datos
        self.seleccion_actual = None
        self.busqueda.set("")

        self.actualizar_tabla()
        self.guardar_datos()

        messagebox.showinfo(
            "Importación",
            "Datos importados correctamente.",
            parent=self
        )

    # ======================================
    # CERRAR PROGRAMA
    # ======================================

    def cerrar(self):

        if self.guardar_datos():
            self.destroy()
        else:
            confirmar = messagebox.askyesno(
                "Salir sin guardar",
                "No se pudieron guardar los datos.\n"
                "¿Deseas cerrar de todas formas?",
                parent=self
            )

            if confirmar:
                self.destroy()


# ==================================================
# EJECUTAR APLICACIÓN
# ==================================================

if __name__ == "__main__":
    aplicacion = SistemaPostres()
    aplicacion.mainloop()
