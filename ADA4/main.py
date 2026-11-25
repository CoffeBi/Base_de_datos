
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import time
from pathlib import Path

from secuencial import busqueda_secuencial
from binaria import busqueda_binaria
from hash import busqueda_hash


# =====================================
# CONFIGURACION GENERAL
# =====================================

ARCHIVO = Path(__file__).with_name("datos.json")

FONDO = "#F4F6F5"
AZUL = "#455A64"
BLANCO = "#FFFFFF"
TEXTO = "#37474F"

VERDE = "#C5DCCF"
ROJO = "#E6C5C8"
MORADO = "#DCD3EB"
CELESTE = "#CBDDEB"
GRIS = "#DDE3E8"
NARANJA = "#E6D9C5"

FUENTE = ("Segoe UI", 10)
NEGRITA = ("Segoe UI", 10, "bold")


# =====================================
# ALMACENAMIENTO DE DATOS
# =====================================

def cargar_datos():
    if ARCHIVO.exists():
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    return {
        "alumnos": [],
        "matriculas": [],
        "productos": {}
    }


def guardar_datos():
    try:
        temporal = ARCHIVO.with_suffix(".tmp")

        with open(temporal, "w", encoding="utf-8") as archivo:
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

        temporal.replace(ARCHIVO)
        return True

    except OSError as error:
        messagebox.showerror(
            "Error al guardar",
            str(error)
        )
        return False


def guardar():
    if guardar_datos():
        estado.set("Datos guardados correctamente")

        messagebox.showinfo(
            "Guardar",
            "Todos los datos fueron guardados."
        )


def actualizar(nuevos_datos):
    grupo = obtener_grupo()
    anteriores = datos[grupo]

    datos[grupo] = nuevos_datos

    if guardar_datos():
        mostrar()
        limpiar()
        resultado.set("Sin búsquedas recientes")
        return True

    datos[grupo] = anteriores
    return False


# =====================================
# IDENTIFICAR METODO
# =====================================

def obtener_grupo():
    opciones = {
        "Secuencial - Alumnos": "alumnos",
        "Binaria - Matrículas": "matriculas",
        "Hash - Productos": "productos"
    }

    return opciones[metodo.get()]


# =====================================
# LIMPIAR CAMPOS
# =====================================

def limpiar():
    entrada_dato.delete(0, tk.END)
    entrada_codigo.delete(0, tk.END)
    entrada_busqueda.delete(0, tk.END)

    seleccion = tabla.selection()

    if seleccion:
        tabla.selection_remove(*seleccion)

    entrada_dato.focus_set()


# =====================================
# CAMBIAR METODO
# =====================================

def cambiar_metodo(evento=None):
    grupo = obtener_grupo()

    limpiar()

    if grupo == "alumnos":

        etiqueta_dato.config(
            text="Nombre del alumno:"
        )

        etiqueta_busqueda.config(
            text="Buscar alumno:"
        )

        etiqueta_codigo.grid_remove()
        entrada_codigo.grid_remove()

        descripcion.set(
            "Búsqueda secuencial | Complejidad O(n)"
        )

    elif grupo == "matriculas":

        etiqueta_dato.config(
            text="Número de matrícula:"
        )

        etiqueta_busqueda.config(
            text="Buscar matrícula:"
        )

        etiqueta_codigo.grid_remove()
        entrada_codigo.grid_remove()

        descripcion.set(
            "Búsqueda binaria | Complejidad O(log n)"
        )

    else:

        etiqueta_dato.config(
            text="Nombre del producto:"
        )

        etiqueta_busqueda.config(
            text="Buscar por código:"
        )

        etiqueta_codigo.grid()
        entrada_codigo.grid()

        descripcion.set(
            "Búsqueda hash | Complejidad promedio O(1)"
        )

    resultado.set("Sin búsquedas realizadas")
    mostrar()


# =====================================
# MOSTRAR REGISTROS
# =====================================

def mostrar():
    for elemento in tabla.get_children():
        tabla.delete(elemento)

    grupo = obtener_grupo()

    if grupo == "productos":

        tabla.heading("clave", text="Código")
        tabla.heading("registro", text="Producto")

        for i, (codigo, nombre) in enumerate(
            datos["productos"].items()
        ):

            etiqueta = "par" if i % 2 == 0 else "impar"

            tabla.insert(
                "",
                "end",
                iid="p:" + codigo,
                values=(codigo, nombre),
                tags=(etiqueta,)
            )

    else:

        tabla.heading("clave", text="Posición")

        if grupo == "alumnos":
            tabla.heading("registro", text="Alumno")
        else:
            tabla.heading("registro", text="Matrícula")

        for i, dato in enumerate(datos[grupo]):

            etiqueta = "par" if i % 2 == 0 else "impar"

            tabla.insert(
                "",
                "end",
                iid=str(i),
                values=(i + 1, dato),
                tags=(etiqueta,)
            )

    contador.set(
        f"Registros actuales: {len(datos[grupo])}"
    )

    total = (
        len(datos["alumnos"])
        + len(datos["matriculas"])
        + len(datos["productos"])
    )

    total_registros.set(
        f"Total general: {total}"
    )

    estado.set("Registros actualizados")


# =====================================
# VALIDAR MATRICULAS
# =====================================

def validar_matricula(valor):
    try:
        numero = int(valor)

        if numero <= 0:
            raise ValueError

        return numero

    except ValueError:

        messagebox.showwarning(
            "Dato incorrecto",
            "Ingresa una matrícula numérica positiva."
        )

        return None


# =====================================
# AGREGAR REGISTROS
# =====================================

def agregar():
    grupo = obtener_grupo()

    valor = entrada_dato.get().strip()
    codigo = entrada_codigo.get().strip()

    nuevos = datos[grupo].copy()

    if not valor:
        messagebox.showwarning(
            "Campos vacíos",
            "Ingresa un dato antes de continuar."
        )
        return

    # Agregar alumno

    if grupo == "alumnos":

        posicion, _ = busqueda_secuencial(
            nuevos,
            valor
        )

        if posicion != -1:
            messagebox.showwarning(
                "Duplicado",
                "El alumno ya está registrado."
            )
            return

        nuevos.append(valor)

    # Agregar matricula

    elif grupo == "matriculas":

        matricula = validar_matricula(valor)

        if matricula is None:
            return

        posicion, _ = busqueda_binaria(
            nuevos,
            matricula
        )

        if posicion != -1:
            messagebox.showwarning(
                "Duplicado",
                "La matrícula ya existe."
            )
            return

        nuevos.append(matricula)
        nuevos.sort()

    # Agregar producto

    else:

        if not codigo:
            messagebox.showwarning(
                "Campos vacíos",
                "Ingresa el código del producto."
            )
            return

        if codigo in nuevos:
            messagebox.showwarning(
                "Duplicado",
                "El código ya está registrado."
            )
            return

        nuevos[codigo] = valor

    if actualizar(nuevos):
        estado.set("Registro agregado y guardado")


# =====================================
# BUSCAR REGISTROS
# =====================================

def buscar():
    grupo = obtener_grupo()
    objetivo = entrada_busqueda.get().strip()

    if not objetivo:
        messagebox.showwarning(
            "Búsqueda",
            "Ingresa el dato que deseas buscar."
        )
        return

    clave = None
    comparaciones = None

    if grupo == "matriculas":

        objetivo = validar_matricula(objetivo)

        if objetivo is None:
            return

    inicio = time.perf_counter_ns()

    # Busqueda secuencial

    if grupo == "alumnos":

        posicion, comparaciones = busqueda_secuencial(
            datos["alumnos"],
            objetivo
        )

        if posicion != -1:
            clave = str(posicion)

    # Busqueda binaria

    elif grupo == "matriculas":

        posicion, comparaciones = busqueda_binaria(
            datos["matriculas"],
            objetivo
        )

        if posicion != -1:
            clave = str(posicion)

    # Busqueda hash

    else:

        encontrado = busqueda_hash(
            datos["productos"],
            objetivo
        )

        if encontrado is not None:
            clave = "p:" + objetivo

    fin = time.perf_counter_ns()

    tiempo = (fin - inicio) / 1000

    mostrar()

    if comparaciones is None:
        texto_comparaciones = "No disponibles (hash)"
    else:
        texto_comparaciones = str(comparaciones)

    if clave is not None:

        tabla.selection_set(clave)
        tabla.focus(clave)
        tabla.see(clave)

        resultado.set(
            f"Encontrado | Comparaciones: "
            f"{texto_comparaciones} | "
            f"Tiempo: {tiempo:.3f} µs"
        )

        estado.set("Búsqueda exitosa")

    else:

        resultado.set(
            f"No encontrado | Comparaciones: "
            f"{texto_comparaciones} | "
            f"Tiempo: {tiempo:.3f} µs"
        )

        estado.set("Registro no encontrado")

        messagebox.showinfo(
            "Búsqueda",
            "El registro solicitado no existe."
        )


# =====================================
# SELECCIONAR REGISTRO
# =====================================

def seleccionar(evento=None):

    seleccion = tabla.selection()

    if not seleccion:
        return

    grupo = obtener_grupo()
    clave = seleccion[0]

    entrada_dato.delete(0, tk.END)
    entrada_codigo.delete(0, tk.END)

    if grupo == "productos":

        codigo = clave[2:]

        entrada_codigo.insert(0, codigo)

        entrada_dato.insert(
            0,
            datos["productos"][codigo]
        )

    else:

        entrada_dato.insert(
            0,
            datos[grupo][int(clave)]
        )


# =====================================
# EDITAR REGISTROS
# =====================================

def editar():

    seleccion = tabla.selection()

    if not seleccion:
        messagebox.showwarning(
            "Editar",
            "Selecciona un registro de la tabla."
        )
        return

    grupo = obtener_grupo()
    clave = seleccion[0]

    nuevo_valor = entrada_dato.get().strip()
    nuevo_codigo = entrada_codigo.get().strip()

    nuevos = datos[grupo].copy()

    if not nuevo_valor:
        messagebox.showwarning(
            "Editar",
            "El nuevo dato no puede estar vacío."
        )
        return

    if grupo == "alumnos":

        posicion = int(clave)

        for i, nombre in enumerate(nuevos):

            if i != posicion and (
                nombre.casefold() == nuevo_valor.casefold()
            ):

                messagebox.showwarning(
                    "Duplicado",
                    "El nombre ya existe."
                )
                return

        nuevos[posicion] = nuevo_valor

    elif grupo == "matriculas":

        matricula = validar_matricula(nuevo_valor)

        if matricula is None:
            return

        posicion = int(clave)

        if matricula in nuevos and (
            matricula != nuevos[posicion]
        ):

            messagebox.showwarning(
                "Duplicado",
                "La matrícula ya existe."
            )
            return

        nuevos[posicion] = matricula
        nuevos.sort()

    else:

        codigo_anterior = clave[2:]

        if not nuevo_codigo:
            messagebox.showwarning(
                "Editar",
                "El código no puede estar vacío."
            )
            return

        if nuevo_codigo in nuevos and (
            nuevo_codigo != codigo_anterior
        ):

            messagebox.showwarning(
                "Duplicado",
                "El código ya existe."
            )
            return

        del nuevos[codigo_anterior]

        nuevos[nuevo_codigo] = nuevo_valor

    if actualizar(nuevos):
        estado.set("Registro editado correctamente")


# =====================================
# ELIMINAR REGISTRO
# =====================================

def eliminar():

    seleccion = tabla.selection()

    if not seleccion:
        messagebox.showwarning(
            "Eliminar",
            "Selecciona el registro que deseas eliminar."
        )
        return

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        "¿Deseas eliminar el registro seleccionado?"
    )

    if not confirmar:
        return

    grupo = obtener_grupo()
    clave = seleccion[0]

    nuevos = datos[grupo].copy()

    if grupo == "productos":
        del nuevos[clave[2:]]

    else:
        nuevos.pop(int(clave))

    if actualizar(nuevos):
        estado.set("Registro eliminado correctamente")


# =====================================
# ELIMINAR TODOS
# =====================================

def eliminar_todos():

    grupo = obtener_grupo()

    if not datos[grupo]:

        messagebox.showinfo(
            "Eliminar",
            "No existen registros para eliminar."
        )
        return

    confirmar = messagebox.askyesno(
        "Eliminar todos",
        f"¿Deseas eliminar todos los registros de {grupo}?"
        "\n\nEsta acción no se puede deshacer."
    )

    if not confirmar:
        return

    nuevos = {} if grupo == "productos" else []

    if actualizar(nuevos):
        resultado.set("Sin búsquedas realizadas")
        estado.set("Todos los registros fueron eliminados")


# =====================================
# EXPORTAR ARCHIVO CSV
# =====================================

def exportar():

    grupo = obtener_grupo()

    if not datos[grupo]:

        messagebox.showwarning(
            "Exportar",
            "No existen registros para exportar."
        )
        return

    ruta = filedialog.asksaveasfilename(
        defaultextension=".csv",
        initialfile=grupo + ".csv",
        filetypes=[
            ("Archivo CSV", "*.csv")
        ]
    )

    if not ruta:
        return

    try:

        with open(
            ruta,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as archivo:

            escritor = csv.writer(archivo)

            if grupo == "productos":

                escritor.writerow(
                    ["Código", "Producto"]
                )

                for codigo, nombre in datos[grupo].items():
                    escritor.writerow([codigo, nombre])

            else:

                encabezado = (
                    "Alumno"
                    if grupo == "alumnos"
                    else "Matrícula"
                )

                escritor.writerow(
                    ["Posición", encabezado]
                )

                for i, dato in enumerate(datos[grupo], 1):
                    escritor.writerow([i, dato])

        messagebox.showinfo(
            "Exportar",
            "Archivo CSV generado correctamente."
        )

        estado.set("Registros exportados")

    except OSError as error:

        messagebox.showerror(
            "Error al exportar",
            str(error)
        )


# =====================================
# INFORMACION DEL PROGRAMA
# =====================================

def informacion():

    messagebox.showinfo(
        "Acerca del programa",
        "ADA4 - Métodos de búsqueda\n\n"
        "Materia: Estructura de datos\n"
        "Unidad 6\n\n"
        "Secuencial: Alumnos\n"
        "Binaria: Matrículas\n"
        "Hash: Productos\n\n"
        "Desarrollado en Python y Tkinter.\n"
        "Almacenamiento permanente en JSON."
    )


# =====================================
# CERRAR PROGRAMA
# =====================================

def salir():

    confirmar = messagebox.askyesno(
        "Salir",
        "¿Deseas cerrar el programa?"
    )

    if confirmar and guardar_datos():
        ventana.destroy()


# =====================================
# VENTANA PRINCIPAL
# =====================================

ventana = tk.Tk()

ventana.title("ADA4 | Sistema de registros")
ventana.configure(bg=FONDO)

# Ajustar tamaño según la pantalla

ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

ancho = min(960, int(ancho_pantalla * 0.85))
alto = min(580, int(alto_pantalla * 0.80))

x = (ancho_pantalla - ancho) // 2
y = (alto_pantalla - alto) // 2

ventana.geometry(
    f"{ancho}x{alto}+{x}+{y}"
)

ventana.minsize(
    min(760, ancho),
    min(480, alto)
)

ventana.option_add("*Font", FUENTE)

try:
    datos = cargar_datos()

    # Mantener las matriculas ordenadas
    datos["matriculas"].sort()

except (OSError, ValueError, KeyError, TypeError) as error:

    messagebox.showerror(
        "Error al cargar los datos",
        str(error)
    )

    ventana.destroy()
    raise SystemExit


# =====================================
# VARIABLES GRAFICAS
# =====================================

metodo = tk.StringVar(
    value="Secuencial - Alumnos"
)

descripcion = tk.StringVar()
contador = tk.StringVar()
total_registros = tk.StringVar()

estado = tk.StringVar(
    value="Sistema listo"
)

resultado = tk.StringVar(
    value="Sin búsquedas realizadas"
)


# =====================================
# ESTILOS
# =====================================

estilo = ttk.Style()
estilo.theme_use("clam")

estilo.configure(
    "Treeview",
    background=BLANCO,
    foreground=TEXTO,
    fieldbackground=BLANCO,
    font=FUENTE,
    rowheight=24,
    borderwidth=0
)

estilo.configure(
    "Treeview.Heading",
    background="#DFE7E8",
    foreground=AZUL,
    font=NEGRITA,
    relief="flat"
)

estilo.map(
    "Treeview",
    background=[
        ("selected", "#C5DCCF")
    ],
    foreground=[
        ("selected", "#344E41")
    ]
)

estilo.configure(
    "TEntry",
    padding=3
)

estilo.configure(
    "TCombobox",
    padding=3
)


# =====================================
# BARRA DE MENU
# =====================================

barra_menu = tk.Menu(ventana)

menu_archivo = tk.Menu(
    barra_menu,
    tearoff=0
)

menu_archivo.add_command(
    label="Guardar datos",
    command=guardar
)

menu_archivo.add_command(
    label="Exportar CSV",
    command=exportar
)

menu_archivo.add_separator()

menu_archivo.add_command(
    label="Salir",
    command=salir
)

barra_menu.add_cascade(
    label="Archivo",
    menu=menu_archivo
)

menu_registros = tk.Menu(
    barra_menu,
    tearoff=0
)

menu_registros.add_command(
    label="Agregar",
    command=agregar
)

menu_registros.add_command(
    label="Editar",
    command=editar
)

menu_registros.add_command(
    label="Eliminar",
    command=eliminar
)

menu_registros.add_command(
    label="Mostrar todos",
    command=mostrar
)

menu_registros.add_separator()

menu_registros.add_command(
    label="Eliminar todos",
    command=eliminar_todos
)

barra_menu.add_cascade(
    label="Registros",
    menu=menu_registros
)

menu_ayuda = tk.Menu(
    barra_menu,
    tearoff=0
)

menu_ayuda.add_command(
    label="Acerca del programa",
    command=informacion
)

barra_menu.add_cascade(
    label="Ayuda",
    menu=menu_ayuda
)

ventana.config(menu=barra_menu)


# =====================================
# FUNCION PARA CREAR BOTONES
# =====================================

def crear_boton(padre, texto, comando, color):

    return tk.Button(
        padre,
        text=texto,
        command=comando,
        bg=color,
        fg=TEXTO,
        activebackground="#D3DFDB",
        activeforeground=TEXTO,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        cursor="hand2",
        bd=0,
        padx=8,
        pady=4
    )


# =====================================
# ENCABEZADO COMPACTO
# =====================================

encabezado = tk.Frame(
    ventana,
    bg=AZUL
)

encabezado.pack(fill="x")

tk.Label(
    encabezado,
    text="Sistema de gestión de registros",
    font=("Segoe UI", 17, "bold"),
    bg=AZUL,
    fg=BLANCO
).pack(pady=(8, 1))

tk.Label(
    encabezado,
    text="ADA4 · Estructura de datos",
    font=("Segoe UI", 9),
    bg=AZUL,
    fg="#DCE5E8"
).pack(pady=(0, 8))


# =====================================
# BARRA INFERIOR
# =====================================

pie = tk.Frame(
    ventana,
    bg=AZUL
)

pie.pack(
    side="bottom",
    fill="x"
)

tk.Label(
    pie,
    textvariable=estado,
    bg=AZUL,
    fg=BLANCO,
    font=("Segoe UI", 9),
    padx=10,
    pady=5
).pack(side="left")

crear_boton(
    pie,
    "Salir",
    salir,
    ROJO
).pack(
    side="right",
    padx=8,
    pady=4
)


# =====================================
# CONTENEDOR PRINCIPAL
# =====================================

principal = tk.Frame(
    ventana,
    bg=FONDO
)

principal.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=8
)

principal.columnconfigure(0, weight=0)
principal.columnconfigure(1, weight=1)
principal.rowconfigure(0, weight=1)


# =====================================
# PANEL IZQUIERDO
# =====================================

panel = tk.Frame(
    principal,
    bg=BLANCO,
    padx=10,
    pady=8,
    highlightbackground="#DCE4E1",
    highlightthickness=1
)

panel.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 10)
)

panel.columnconfigure(0, weight=1)

tk.Label(
    panel,
    text="Panel de control",
    font=("Segoe UI", 13, "bold"),
    bg=BLANCO,
    fg=AZUL
).grid(
    row=0,
    column=0,
    pady=(0, 6)
)

tk.Label(
    panel,
    text="Método de búsqueda:",
    bg=BLANCO,
    fg=TEXTO,
    font=NEGRITA
).grid(
    row=1,
    column=0,
    sticky="w"
)

selector = ttk.Combobox(
    panel,
    textvariable=metodo,
    values=[
        "Secuencial - Alumnos",
        "Binaria - Matrículas",
        "Hash - Productos"
    ],
    state="readonly",
    width=23,
    font=FUENTE
)

selector.grid(
    row=2,
    column=0,
    sticky="ew",
    pady=(3, 6)
)

selector.bind(
    "<<ComboboxSelected>>",
    cambiar_metodo
)


# =====================================
# CAMPOS DE CAPTURA
# =====================================

etiqueta_codigo = tk.Label(
    panel,
    text="Código del producto:",
    bg=BLANCO,
    fg=TEXTO,
    font=NEGRITA
)

etiqueta_codigo.grid(
    row=3,
    column=0,
    sticky="w"
)

entrada_codigo = ttk.Entry(
    panel,
    font=FUENTE
)

entrada_codigo.grid(
    row=4,
    column=0,
    sticky="ew",
    pady=(3, 5)
)

etiqueta_dato = tk.Label(
    panel,
    text="Nombre del alumno:",
    bg=BLANCO,
    fg=TEXTO,
    font=NEGRITA
)

etiqueta_dato.grid(
    row=5,
    column=0,
    sticky="w"
)

entrada_dato = ttk.Entry(
    panel,
    font=FUENTE
)

entrada_dato.grid(
    row=6,
    column=0,
    sticky="ew",
    pady=(3, 6)
)


# =====================================
# BOTONES DEL PANEL
# =====================================

marco_botones = tk.Frame(
    panel,
    bg=BLANCO
)

marco_botones.grid(
    row=7,
    column=0,
    sticky="ew"
)

marco_botones.columnconfigure(0, weight=1)
marco_botones.columnconfigure(1, weight=1)

opciones = [
    ("Agregar", agregar, VERDE),
    ("Editar", editar, NARANJA),
    ("Eliminar", eliminar, ROJO),
    ("Limpiar", limpiar, GRIS),
    ("Guardar", guardar, MORADO),
    ("Exportar", exportar, CELESTE)
]

for i, (texto, comando, color) in enumerate(opciones):

    crear_boton(
        marco_botones,
        texto,
        comando,
        color
    ).grid(
        row=i // 2,
        column=i % 2,
        sticky="ew",
        padx=2,
        pady=3
    )

crear_boton(
    panel,
    "Eliminar todos los registros",
    eliminar_todos,
    "#DFC1C5"
).grid(
    row=8,
    column=0,
    sticky="ew",
    pady=(5, 3)
)

ttk.Separator(
    panel,
    orient="horizontal"
).grid(
    row=9,
    column=0,
    sticky="ew",
    pady=8
)

tk.Label(
    panel,
    text="Guardado automático activado",
    bg=BLANCO,
    fg="#648575",
    font=("Segoe UI", 9),
    wraplength=200
).grid(
    row=10,
    column=0,
    pady=3
)


# =====================================
# PANEL DERECHO
# =====================================

contenido = tk.Frame(
    principal,
    bg=FONDO
)

contenido.grid(
    row=0,
    column=1,
    sticky="nsew"
)

contenido.columnconfigure(0, weight=1)
contenido.rowconfigure(3, weight=1)

tk.Label(
    contenido,
    text="Registros almacenados",
    font=("Segoe UI", 14, "bold"),
    bg=FONDO,
    fg=AZUL
).grid(
    row=0,
    column=0,
    sticky="w"
)

tk.Label(
    contenido,
    textvariable=descripcion,
    font=("Segoe UI", 9),
    bg=FONDO,
    fg="#75858D"
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=(2, 6)
)


# =====================================
# BUSCADOR
# =====================================

marco_busqueda = tk.Frame(
    contenido,
    bg=BLANCO,
    padx=8,
    pady=6
)

marco_busqueda.grid(
    row=2,
    column=0,
    sticky="ew"
)

marco_busqueda.columnconfigure(0, weight=1)

etiqueta_busqueda = tk.Label(
    marco_busqueda,
    text="Buscar alumno:",
    bg=BLANCO,
    fg=TEXTO,
    font=NEGRITA
)

etiqueta_busqueda.grid(
    row=0,
    column=0,
    columnspan=3,
    sticky="w"
)

entrada_busqueda = ttk.Entry(
    marco_busqueda,
    font=FUENTE
)

entrada_busqueda.grid(
    row=1,
    column=0,
    sticky="ew",
    pady=(4, 0)
)

crear_boton(
    marco_busqueda,
    "Buscar",
    buscar,
    CELESTE
).grid(
    row=1,
    column=1,
    padx=4,
    pady=(4, 0)
)

crear_boton(
    marco_busqueda,
    "Mostrar todos",
    mostrar,
    GRIS
).grid(
    row=1,
    column=2,
    pady=(4, 0)
)


# =====================================
# TABLA DE REGISTROS
# =====================================

marco_tabla = tk.Frame(
    contenido,
    bg=BLANCO,
    highlightbackground="#DCE4E1",
    highlightthickness=1
)

marco_tabla.grid(
    row=3,
    column=0,
    sticky="nsew",
    pady=7
)

marco_tabla.columnconfigure(0, weight=1)
marco_tabla.rowconfigure(0, weight=1)

tabla = ttk.Treeview(
    marco_tabla,
    columns=("clave", "registro"),
    show="headings",
    selectmode="browse",
    height=5
)

tabla.heading(
    "clave",
    text="Posición"
)

tabla.heading(
    "registro",
    text="Registro"
)

tabla.column(
    "clave",
    width=90,
    minwidth=65,
    anchor="center",
    stretch=False
)

tabla.column(
    "registro",
    width=250,
    minwidth=120,
    anchor="center",
    stretch=True
)

# Colores alternados de las filas

tabla.tag_configure(
    "par",
    background="#FFFFFF"
)

tabla.tag_configure(
    "impar",
    background="#F0F5F3"
)

barra = ttk.Scrollbar(
    marco_tabla,
    orient="vertical",
    command=tabla.yview
)

tabla.configure(
    yscrollcommand=barra.set
)

tabla.grid(
    row=0,
    column=0,
    sticky="nsew"
)

barra.grid(
    row=0,
    column=1,
    sticky="ns"
)

tabla.bind(
    "<<TreeviewSelect>>",
    seleccionar
)


# =====================================
# ESTADISTICAS DE BUSQUEDA
# =====================================

estadisticas = tk.Frame(
    contenido,
    bg=BLANCO,
    padx=8,
    pady=6,
    highlightbackground="#DCE4E1",
    highlightthickness=1
)

estadisticas.grid(
    row=4,
    column=0,
    sticky="ew"
)

estadisticas.columnconfigure(0, weight=1)
estadisticas.columnconfigure(1, weight=1)

tk.Label(
    estadisticas,
    text="Estadísticas de búsqueda",
    font=("Segoe UI", 11, "bold"),
    bg=BLANCO,
    fg=AZUL
).grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="w"
)

etiqueta_resultado = tk.Label(
    estadisticas,
    textvariable=resultado,
    font=("Segoe UI", 9),
    bg=BLANCO,
    fg="#607D8B",
    wraplength=400,
    justify="left"
)

etiqueta_resultado.grid(
    row=1,
    column=0,
    columnspan=2,
    sticky="w",
    pady=4
)

estadisticas.bind(
    "<Configure>",
    lambda evento: etiqueta_resultado.config(
        wraplength=max(100, evento.width - 20)
    )
)

tk.Label(
    estadisticas,
    textvariable=contador,
    font=("Segoe UI", 9, "bold"),
    bg=BLANCO,
    fg="#648575"
).grid(
    row=2,
    column=0,
    sticky="w"
)

tk.Label(
    estadisticas,
    textvariable=total_registros,
    font=("Segoe UI", 9),
    bg=BLANCO,
    fg=AZUL
).grid(
    row=2,
    column=1,
    sticky="e"
)


# =====================================
# ATAJOS DE TECLADO
# =====================================

entrada_busqueda.bind(
    "<Return>",
    lambda evento: buscar()
)

entrada_dato.bind(
    "<Return>",
    lambda evento: agregar()
)

ventana.bind(
    "<Control-s>",
    lambda evento: guardar()
)

ventana.bind(
    "<Escape>",
    lambda evento: limpiar()
)

ventana.protocol(
    "WM_DELETE_WINDOW",
    salir
)


# =====================================
# INICIAR PROGRAMA
# =====================================

cambiar_metodo()

ventana.mainloop()
