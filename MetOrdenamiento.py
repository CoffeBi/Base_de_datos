import tkinter as tk
from tkinter import ttk, messagebox


# ==============================================================================
# ALGORITMOS DE ORDENAMIENTO
# ==============================================================================
def shell_sort(arr):
    lista = arr.copy()
    n = len(lista)
    brecha = n // 2
    while brecha > 0:
        for i in range(brecha, n):
            temp = lista[i]
            j = i
            while j >= brecha and lista[j - brecha] > temp:
                lista[j] = lista[j - brecha]
                j -= brecha
            lista[j] = temp
        brecha //= 2
    return lista


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivote = arr[len(arr) // 2]
    izquierda = [x for x in arr if x < pivote]
    centro = [x for x in arr if x == pivote]
    derecha = [x for x in arr if x > pivote]
    return quick_sort(izquierda) + centro + quick_sort(derecha)


def heapify(lista, n, i):
    mayor = i
    izq = 2 * i + 1
    der = 2 * i + 2

    if izq < n and lista[izq] > lista[mayor]:
        mayor = izq
    if der < n and lista[der] > lista[mayor]:
        mayor = der

    if mayor != i:
        lista[i], lista[mayor] = lista[mayor], lista[i]
        heapify(lista, n, mayor)


def heap_sort(arr):
    lista = arr.copy()
    n = len(lista)
    for i in range(n // 2 - 1, -1, -1):
        heapify(lista, n, i)
    for i in range(n - 1, 0, -1):
        lista[i], lista[0] = lista[0], lista[i]
        heapify(lista, i, 0)
    return lista


def counting_sort_radix(lista, exp):
    n = len(lista)
    salida = [0] * n
    conteo = [0] * 10

    for i in range(n):
        indice = (lista[i] // exp) % 10
        conteo[indice] += 1

    for i in range(1, 10):
        conteo[i] += conteo[i - 1]

    i = n - 1
    while i >= 0:
        indice = (lista[i] // exp) % 10
        salida[conteo[indice] - 1] = lista[i]
        conteo[indice] -= 1
        i -= 1

    for i in range(n):
        lista[i] = salida[i]


def _radix_positivos(arr):
    if not arr:
        return []
    lista = arr.copy()
    maximo = max(lista)
    exp = 1
    while maximo // exp > 0:
        counting_sort_radix(lista, exp)
        exp *= 10
    return lista


def radix_sort(arr):
    if not arr:
        return []
    negativos = [-x for x in arr if x < 0]
    positivos = [x for x in arr if x >= 0]
    negativos_ord = [-x for x in reversed(_radix_positivos(negativos))]
    positivos_ord = _radix_positivos(positivos)
    return negativos_ord + positivos_ord


# ==============================================================================
# INTERFAZ GRÁFICA (TKINTER) CON PANTALLA COMPLETA
# ==============================================================================
class AplicacionOrdenamiento:
    def __init__(self, root):
        self.root = root
        self.root.title("ADA 2 - Métodos de Ordenamiento")
        self.root.geometry("680x580")
        self.root.minsize(540, 520)  # Permite maximizar y redimensionar libremente
        self.root.configure(bg="#1e1e2e")

        # Estado de pantalla completa
        self.pantalla_completa = False

        # Atajos de teclado para pantalla completa
        self.root.bind("<F11>", self.alternar_pantalla_completa)
        self.root.bind("<Escape>", self.salir_pantalla_completa)

        # Paleta de colores
        self.bg_principal = "#1e1e2e"
        self.bg_tarjeta = "#2a2a3c"
        self.color_texto = "#ffffff"
        self.color_subtexto = "#a6adc8"
        self.color_acento = "#89b4fa"
        self.color_exito = "#a6e3a1"
        self.color_salir = "#f38ba8"

        self.crear_widgets()

    def crear_widgets(self):
        # Barra superior para el botón de Pantalla Completa
        barra_top = tk.Frame(self.root, bg=self.bg_principal)
        barra_top.pack(fill="x", padx=25, pady=(15, 0))

        self.btn_fullscreen = tk.Button(
            barra_top,
            text="⛶ Pantalla Completa (F11)",
            font=("Segoe UI", 9, "bold"),
            bg="#313244",
            fg=self.color_texto,
            activebackground="#45475a",
            activeforeground=self.color_texto,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self.alternar_pantalla_completa,
        )
        self.btn_fullscreen.pack(side="right")

        # Contenedor central adaptable
        contenedor_central = tk.Frame(self.root, bg=self.bg_principal)
        contenedor_central.pack(expand=True, fill="both", padx=40, pady=(5, 25))

        # Título principal
        lbl_titulo = tk.Label(
            contenedor_central,
            text="Métodos de Ordenamiento (ADA 2)",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg_principal,
            fg=self.color_acento,
        )
        lbl_titulo.pack(pady=(5, 5))

        lbl_sub = tk.Label(
            contenedor_central,
            text="Selecciona un algoritmo, define la cantidad e ingresa los números",
            font=("Segoe UI", 10),
            bg=self.bg_principal,
            fg=self.color_subtexto,
        )
        lbl_sub.pack(pady=(0, 15))

        # Tarjeta principal
        self.frame_tarjeta = tk.Frame(
            contenedor_central, bg=self.bg_tarjeta, padx=25, pady=25
        )
        self.frame_tarjeta.pack(fill="both", expand=True)

        # 1. Selector de método (Menú)
        tk.Label(
            self.frame_tarjeta,
            text="1. Método de ordenamiento:",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_tarjeta,
            fg=self.color_texto,
        ).pack(anchor="w")

        self.metodo_var = tk.StringVar(value="ShellSort")
        combo_metodos = ttk.Combobox(
            self.frame_tarjeta,
            textvariable=self.metodo_var,
            values=["ShellSort", "Quicksort", "Heapsort", "Radix"],
            state="readonly",
            font=("Segoe UI", 11),
        )
        combo_metodos.pack(fill="x", pady=(5, 15))

        # 2. Cantidad de números
        tk.Label(
            self.frame_tarjeta,
            text="2. Cantidad de números a ingresar:",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_tarjeta,
            fg=self.color_texto,
        ).pack(anchor="w")

        self.entry_cantidad = tk.Entry(
            self.frame_tarjeta,
            font=("Segoe UI", 11),
            bg="#313244",
            fg=self.color_texto,
            insertbackground="white",
            relief="flat",
        )
        self.entry_cantidad.pack(fill="x", ipady=6, pady=(5, 15))

        # 3. Entrada de los números
        tk.Label(
            self.frame_tarjeta,
            text="3. Ingresa los números (separados por espacios o comas):",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_tarjeta,
            fg=self.color_texto,
        ).pack(anchor="w")

        self.entry_numeros = tk.Entry(
            self.frame_tarjeta,
            font=("Segoe UI", 11),
            bg="#313244",
            fg=self.color_texto,
            insertbackground="white",
            relief="flat",
        )
        self.entry_numeros.pack(fill="x", ipady=6, pady=(5, 20))

        # Botones de acción
        frame_botones = tk.Frame(self.frame_tarjeta, bg=self.bg_tarjeta)
        frame_botones.pack(fill="x", pady=(0, 20))

        btn_ordenar = tk.Button(
            frame_botones,
            text="Ordenar Lista",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_acento,
            fg="#11111b",
            activebackground="#74c7ec",
            relief="flat",
            cursor="hand2",
            command=self.ejecutar_ordenamiento,
        )
        btn_ordenar.pack(side="left", expand=True, fill="x", ipady=8, padx=(0, 6))

        btn_limpiar = tk.Button(
            frame_botones,
            text="Limpiar",
            font=("Segoe UI", 10, "bold"),
            bg="#45475a",
            fg=self.color_texto,
            activebackground="#585b70",
            relief="flat",
            cursor="hand2",
            command=self.limpiar_campos,
        )
        btn_limpiar.pack(side="left", expand=True, fill="x", ipady=8, padx=6)

        btn_salir = tk.Button(
            frame_botones,
            text="Salir",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_salir,
            fg="#11111b",
            activebackground="#eba0ac",
            relief="flat",
            cursor="hand2",
            command=self.salir_app,
        )
        btn_salir.pack(side="left", expand=True, fill="x", ipady=8, padx=(6, 0))

        # Área de resultados con ajuste dinámico de ancho
        self.lbl_original = tk.Label(
            self.frame_tarjeta,
            text="Lista original: -",
            font=("Segoe UI", 11),
            bg=self.bg_tarjeta,
            fg=self.color_subtexto,
            justify="left",
            anchor="w",
        )
        self.lbl_original.pack(fill="x", pady=(5, 8))

        self.lbl_resultado = tk.Label(
            self.frame_tarjeta,
            text="Lista ordenada: -",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_tarjeta,
            fg=self.color_exito,
            justify="left",
            anchor="w",
        )
        self.lbl_resultado.pack(fill="x", pady=(5, 0))

        # Ajustar el salto de línea (wraplength) cuando cambie el tamaño de la ventana
        self.frame_tarjeta.bind("<Configure>", self.ajustar_wraplength)

    def ajustar_wraplength(self, event):
        nuevo_ancho = max(event.width - 50, 300)
        self.lbl_original.config(wraplength=nuevo_ancho)
        self.lbl_resultado.config(wraplength=nuevo_ancho)

    def alternar_pantalla_completa(self, event=None):
        self.pantalla_completa = not self.pantalla_completa
        self.root.attributes("-fullscreen", self.pantalla_completa)
        if self.pantalla_completa:
            self.btn_fullscreen.config(text="🗗 Salir de Pantalla Completa (Esc)")
        else:
            self.btn_fullscreen.config(text="⛶ Pantalla Completa (F11)")

    def salir_pantalla_completa(self, event=None):
        if self.pantalla_completa:
            self.pantalla_completa = False
            self.root.attributes("-fullscreen", False)
            self.btn_fullscreen.config(text="⛶ Pantalla Completa (F11)")

    def ejecutar_ordenamiento(self):
        try:
            cantidad = int(self.entry_cantidad.get().strip())
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número entero válido en 'Cantidad'.")
            return

        texto_numeros = self.entry_numeros.get().replace(",", " ").strip()
        if not texto_numeros:
            messagebox.showerror("Error", "Por favor ingresa los números a ordenar.")
            return

        partes = texto_numeros.split()
        try:
            numeros = [int(x) for x in partes]
        except ValueError:
            messagebox.showerror(
                "Error",
                "Asegúrate de ingresar solo números enteros separados por espacio o coma.",
            )
            return

        if len(numeros) != cantidad:
            messagebox.showwarning(
                "Cantidad no coincide",
                f"Indicaste {cantidad} números, pero ingresaste {len(numeros)}.\n"
                "Ajusta la cantidad o los números para continuar.",
            )
            return

        metodo = self.metodo_var.get()
        if metodo == "ShellSort":
            ordenados = shell_sort(numeros)
        elif metodo == "Quicksort":
            ordenados = quick_sort(numeros)
        elif metodo == "Heapsort":
            ordenados = heap_sort(numeros)
        elif metodo == "Radix":
            ordenados = radix_sort(numeros)

        self.lbl_original.config(text=f"Lista original ({cantidad} elementos): {numeros}")
        self.lbl_resultado.config(text=f"Lista ordenada ({metodo}): {ordenados}")

    def limpiar_campos(self):
        self.entry_cantidad.delete(0, tk.END)
        self.entry_numeros.delete(0, tk.END)
        self.lbl_original.config(text="Lista original: -")
        self.lbl_resultado.config(text="Lista ordenada: -")

    def salir_app(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar el programa?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionOrdenamiento(root)
    root.mainloop()