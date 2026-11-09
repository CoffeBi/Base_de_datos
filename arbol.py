
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from xml.sax.saxutils import escape

# ==========================
# COLORES
# ==========================

BG = '#101827'
PANEL = '#1a2940'
CANVAS_BG = '#0c1625'
TEXT = '#f2f6ff'
MUTED = '#aebed4'
BLUE = '#72aaff'
GREEN = '#62d8ae'
YELLOW = '#ffcc70'
RED = '#ff8190'
EDGE = '#7188a9'


# ==========================
# CLASE NODO
# ==========================

class Nodo:
    def __init__(self, valor, padre=None):
        self.valor = str(valor)
        self.padre = padre
        self.izquierdo = None
        self.derecho = None


# ==========================
# APLICACIÓN PRINCIPAL
# ==========================

class ArbolApp:

    def __init__(self, root):
        self.root = root

        root.title('Laboratorio de árbol binario')
        root.geometry('1220x780')
        root.minsize(820, 570)
        root.configure(bg=BG)

        self.raiz = None
        self.seleccionado = None

        self.posiciones = {}
        self.escala = 1.0

        # Variables para arrastrar nodos
        self.origen_drag = None
        self.inicio_drag = None
        self.arrastrando = False
        self.destino_drag = None
        self.lado_drag = None

        # Animaciones
        self.resaltado = None
        self.animacion_id = None

        # Historial
        self.historial = []
        self.futuros = []

        # Variables de interfaz
        self.valor = tk.StringVar()
        self.lado = tk.StringVar(value='izquierdo')

        self.recorrido_texto = tk.StringVar(
            value='Recorrido: —'
        )

        self.estado = tk.StringVar(
            value='Crea la raíz escribiendo un valor y pulsando Agregar.'
        )

        self.info = tk.StringVar(
            value='Nodos: 0 | Altura: 0 | Hojas: 0'
        )

        self.velocidad = tk.IntVar(value=600)

        self.crear_interfaz()
        self.vincular_atajos()
        self.dibujar()

    # ==========================
    # INTERFAZ GRÁFICA
    # ==========================

    def crear_interfaz(self):

        cabecera = tk.Frame(self.root, bg=BG)
        cabecera.pack(
            fill='x',
            padx=15,
            pady=(14, 8)
        )

        tk.Label(
            cabecera,
            text='Árbol binario interactivo',
            bg=BG,
            fg=TEXT,
            font=('DejaVu Sans', 18, 'bold')
        ).pack(anchor='w')

        tk.Label(
            cabecera,
            text='Puedes agregar, eliminar, buscar y mover nodos libremente.',
            bg=BG,
            fg=MUTED
        ).pack(anchor='w')

        panel = tk.Frame(
            self.root,
            bg=PANEL,
            padx=11,
            pady=10
        )

        panel.pack(
            fill='x',
            padx=15,
            pady=(0, 9)
        )

        # Primera fila
        fila1 = tk.Frame(panel, bg=PANEL)
        fila1.pack(fill='x', pady=(0, 8))

        tk.Label(
            fila1,
            text='Valor:',
            bg=PANEL,
            fg=TEXT
        ).pack(side='left')

        self.entrada = tk.Entry(
            fila1,
            textvariable=self.valor,
            width=13,
            bg='#293d58',
            fg=TEXT,
            insertbackground=TEXT,
            relief='flat',
            font=('DejaVu Sans', 11)
        )

        self.entrada.pack(
            side='left',
            padx=(5, 9),
            ipady=5
        )

        ttk.Combobox(
            fila1,
            textvariable=self.lado,
            values=('izquierdo', 'derecho'),
            state='readonly',
            width=12
        ).pack(side='left', padx=(0, 8))

        self.boton(
            fila1, 'Agregar',
            self.agregar, GREEN
        )

        self.boton(
            fila1, 'Eliminar solo nodo',
            self.eliminar_nodo, RED
        )

        self.boton(
            fila1, 'Eliminar rama',
            self.eliminar_rama, RED
        )

        self.boton(
            fila1, 'Cambiar hijos',
            self.intercambiar_hijos, BLUE
        )

        self.boton(
            fila1, 'Buscar',
            self.buscar, BLUE
        )

        # Segunda fila
        fila2 = tk.Frame(panel, bg=PANEL)
        fila2.pack(fill='x', pady=(0, 8))

        self.boton(
            fila2, 'Preorden',
            lambda: self.recorrer('Preorden'),
            BLUE
        )

        self.boton(
            fila2, 'Inorden',
            lambda: self.recorrer('Inorden'),
            BLUE
        )

        self.boton(
            fila2, 'Postorden',
            lambda: self.recorrer('Postorden'),
            BLUE
        )

        self.boton(
            fila2, 'Detener',
            self.detener_animacion,
            YELLOW
        )

        tk.Label(
            fila2,
            text='Intervalo (ms):',
            bg=PANEL,
            fg=TEXT
        ).pack(side='left', padx=(12, 4))

        tk.Scale(
            fila2,
            from_=150,
            to=1500,
            resolution=50,
            variable=self.velocidad,
            orient='horizontal',
            showvalue=True,
            bg=PANEL,
            fg=TEXT,
            highlightthickness=0,
            troughcolor='#39506b',
            length=150
        ).pack(side='left')

        # Tercera fila
        fila3 = tk.Frame(panel, bg=PANEL)
        fila3.pack(fill='x')

        botones = [
            ('Deshacer', self.deshacer, YELLOW),
            ('Rehacer', self.rehacer, YELLOW),
            ('Guardar JSON', self.guardar, GREEN),
            ('Abrir JSON', self.abrir, GREEN),
            ('Exportar SVG', self.exportar_svg, GREEN),
            ('Ejemplo', self.cargar_ejemplo, BLUE),
            ('Vaciar', self.vaciar, RED),
            ('− Zoom', lambda: self.cambiar_zoom(-0.15), BLUE),
            ('+ Zoom', lambda: self.cambiar_zoom(0.15), BLUE)
        ]

        for texto, comando, color in botones:
            self.boton(
                fila3, texto, comando, color
            )

        # Resultado de los recorridos
        tk.Label(
            self.root,
            textvariable=self.recorrido_texto,
            bg=BG,
            fg=GREEN,
            font=('DejaVu Sans', 11, 'bold'),
            anchor='w',
            wraplength=1120,
            justify='left'
        ).pack(
            fill='x',
            padx=16,
            pady=(2, 5)
        )

        # Área para dibujar
        zona = tk.Frame(self.root, bg=BG)
        zona.pack(
            fill='both',
            expand=True,
            padx=15
        )

        self.canvas = tk.Canvas(
            zona,
            bg=CANVAS_BG,
            highlightthickness=0,
            cursor='hand2'
        )

        h = ttk.Scrollbar(
            zona,
            orient='horizontal',
            command=self.canvas.xview
        )

        v = ttk.Scrollbar(
            zona,
            orient='vertical',
            command=self.canvas.yview
        )

        self.canvas.configure(
            xscrollcommand=h.set,
            yscrollcommand=v.set
        )

        zona.grid_rowconfigure(0, weight=1)
        zona.grid_columnconfigure(0, weight=1)

        self.canvas.grid(
            row=0,
            column=0,
            sticky='nsew'
        )

        v.grid(row=0, column=1, sticky='ns')
        h.grid(row=1, column=0, sticky='ew')

        # Eventos del mouse
        self.canvas.bind(
            '<ButtonPress-1>',
            self.mouse_abajo
        )

        self.canvas.bind(
            '<B1-Motion>',
            self.mouse_mover
        )

        self.canvas.bind(
            '<ButtonRelease-1>',
            self.mouse_arriba
        )

        self.canvas.bind(
            '<Configure>',
            lambda event: self.dibujar()
        )

        # Información inferior
        tk.Label(
            self.root,
            textvariable=self.info,
            bg=BG,
            fg=TEXT,
            anchor='w'
        ).pack(
            fill='x',
            padx=16,
            pady=(7, 2)
        )

        tk.Label(
            self.root,
            textvariable=self.estado,
            bg=BG,
            fg=MUTED,
            anchor='w',
            wraplength=1150,
            justify='left'
        ).pack(
            fill='x',
            padx=16,
            pady=(0, 12)
        )

        self.entrada.focus_set()

    # ==========================
    # CREAR BOTONES
    # ==========================

    def boton(self, padre, texto, comando, color):

        tk.Button(
            padre,
            text=texto,
            command=comando,
            bg=color,
            fg='#0b1826',
            activebackground=color,
            relief='flat',
            cursor='hand2',
            font=('DejaVu Sans', 9, 'bold'),
            padx=9,
            pady=5
        ).pack(side='left', padx=(0, 5))

    # ==========================
    # ATAJOS DE TECLADO
    # ==========================

    def vincular_atajos(self):

        self.root.bind(
            '<Control-z>',
            lambda event: self.deshacer()
        )

        self.root.bind(
            '<Control-y>',
            lambda event: self.rehacer()
        )

        self.root.bind(
            '<Control-s>',
            lambda event: self.guardar()
        )

        self.root.bind(
            '<Control-o>',
            lambda event: self.abrir()
        )

        self.root.bind(
            '<Delete>',
            lambda event: self.eliminar_nodo()
            if self.root.focus_get() != self.entrada
            else None
        )

        self.entrada.bind(
            '<Return>',
            lambda event: self.agregar()
        )

    # ==========================
    # SERIALIZAR ÁRBOL
    # ==========================

    def serializar(self, nodo):

        if nodo is None:
            return None

        return {
            'valor': nodo.valor,
            'izquierdo': self.serializar(nodo.izquierdo),
            'derecho': self.serializar(nodo.derecho)
        }

    # ==========================
    # RECONSTRUIR ÁRBOL
    # ==========================

    def reconstruir(self, datos, padre=None):

        if datos is None:
            return None

        if (
            not isinstance(datos, dict)
            or set(datos) != {
                'valor', 'izquierdo', 'derecho'
            }
        ):
            raise ValueError(
                'Estructura de árbol no válida.'
            )

        if not isinstance(datos['valor'], str):
            raise ValueError(
                'El valor del nodo debe ser texto.'
            )

        nodo = Nodo(datos['valor'], padre)

        nodo.izquierdo = self.reconstruir(
            datos['izquierdo'],
            nodo
        )

        nodo.derecho = self.reconstruir(
            datos['derecho'],
            nodo
        )

        return nodo

    # ==========================
    # HISTORIAL
    # ==========================

    def guardar_historial(self):

        self.detener_animacion(redibujar=False)

        self.historial.append(
            self.serializar(self.raiz)
        )

        if len(self.historial) > 80:
            self.historial.pop(0)

        self.futuros.clear()

    def restaurar(self, estado):

        self.detener_animacion(redibujar=False)

        self.raiz = self.reconstruir(estado)
        self.seleccionado = None

        self.recorrido_texto.set('Recorrido: —')
        self.dibujar()

    def deshacer(self):

        if not self.historial:
            self.estado.set(
                'No hay cambios para deshacer.'
            )
            return

        self.futuros.append(
            self.serializar(self.raiz)
        )

        self.restaurar(
            self.historial.pop()
        )

        self.estado.set('Cambio deshecho.')

    def rehacer(self):

        if not self.futuros:
            self.estado.set(
                'No hay cambios para rehacer.'
            )
            return

        self.historial.append(
            self.serializar(self.raiz)
        )

        self.restaurar(
            self.futuros.pop()
        )

        self.estado.set('Cambio rehecho.')

    # ==========================
    # AGREGAR NODO
    # ==========================

    def agregar(self):

        valor = self.valor.get().strip()

        if not valor:
            messagebox.showwarning(
                'Valor vacío',
                'Escribe un valor.'
            )
            return

        if (
            self.raiz is not None
            and self.seleccionado is None
        ):
            messagebox.showwarning(
                'Falta selección',
                'Selecciona el nodo padre.'
            )
            return

        if self.raiz is not None:

            ocupado = getattr(
                self.seleccionado,
                self.lado.get()
            )

            if ocupado is not None:
                messagebox.showwarning(
                    'Posición ocupada',
                    'Ese hijo ya tiene un nodo.'
                )
                return

        self.guardar_historial()

        if self.raiz is None:
            self.raiz = Nodo(valor)
            nuevo = self.raiz

        else:
            nuevo = Nodo(
                valor,
                self.seleccionado
            )

            setattr(
                self.seleccionado,
                self.lado.get(),
                nuevo
            )

        self.seleccionado = nuevo
        self.valor.set('')

        self.recorrido_texto.set('Recorrido: —')
        self.estado.set(f'Agregado: {valor}.')

        self.dibujar()

    # ==========================
    # SEPARAR UN NODO
    # ==========================

    def separar(self, nodo):

        if nodo.padre is None:
            self.raiz = None

        elif nodo.padre.izquierdo is nodo:
            nodo.padre.izquierdo = None

        else:
            nodo.padre.derecho = None

        nodo.padre = None

    # ==========================
    # ELIMINAR RAMA COMPLETA
    # ==========================

    def eliminar_rama(self):

        nodo = self.seleccionado

        if nodo is None:
            messagebox.showinfo(
                'Selecciona',
                'Selecciona un nodo.'
            )
            return

        if nodo.izquierdo or nodo.derecho:

            confirmar = messagebox.askyesno(
                'Eliminar rama',
                '¿Eliminar el nodo y todos sus descendientes?'
            )

            if not confirmar:
                return

        self.guardar_historial()

        padre = nodo.padre

        self.separar(nodo)

        self.seleccionado = padre

        self.recorrido_texto.set('Recorrido: —')
        self.estado.set(
            'Se eliminó la rama seleccionada.'
        )

        self.dibujar()

    # ==========================
    # ELIMINAR SOLO UN NODO
    # SIN PERDER DESCENDIENTES
    # ==========================

    def eliminar_nodo(self):

        nodo = self.seleccionado

        if nodo is None:
            messagebox.showinfo(
                'Selecciona',
                'Selecciona un nodo.'
            )
            return

        self.guardar_historial()

        padre = nodo.padre
        izquierdo = nodo.izquierdo
        derecho = nodo.derecho

        # Caso 1: tiene hijo izquierdo
        if izquierdo is not None:

            reemplazo = izquierdo
            reemplazo.padre = padre

            # Si también tiene hijo derecho,
            # conservamos ambas ramas.
            if derecho is not None:

                extremo = izquierdo

                # Buscar el nodo más a la derecha
                # de la rama izquierda.
                while extremo.derecho is not None:
                    extremo = extremo.derecho

                # Conectar la otra rama
                extremo.derecho = derecho
                derecho.padre = extremo

        # Caso 2: solo tiene hijo derecho
        # o no tiene hijos
        else:

            reemplazo = derecho

            if reemplazo is not None:
                reemplazo.padre = padre

        # Reconectar el reemplazo al padre original
        if padre is None:
            self.raiz = reemplazo

        elif padre.izquierdo is nodo:
            padre.izquierdo = reemplazo

        else:
            padre.derecho = reemplazo

        # Desconectar únicamente el nodo eliminado
        nodo.padre = None
        nodo.izquierdo = None
        nodo.derecho = None

        self.seleccionado = reemplazo or padre

        self.recorrido_texto.set('Recorrido: —')

        self.estado.set(
            'Nodo eliminado correctamente. '
            'Todos sus descendientes se conservaron.'
        )

        self.dibujar()

    # ==========================
    # INTERCAMBIAR HIJOS
    # ==========================

    def intercambiar_hijos(self):

        if self.seleccionado is None:

            messagebox.showinfo(
                'Selecciona',
                'Selecciona un nodo.'
            )
            return

        nodo = self.seleccionado

        if (
            nodo.izquierdo is None
            and nodo.derecho is None
        ):
            self.estado.set(
                'El nodo no tiene hijos que intercambiar.'
            )
            return

        self.guardar_historial()

        nodo.izquierdo, nodo.derecho = (
            nodo.derecho,
            nodo.izquierdo
        )

        self.recorrido_texto.set('Recorrido: —')

        self.estado.set(
            'Hijos izquierdo y derecho intercambiados.'
        )

        self.dibujar()

    # ==========================
    # COMPROBAR ANCESTROS
    # ==========================

    def es_ancestro(self, candidato, nodo):

        while nodo is not None:

            if candidato is nodo:
                return True

            nodo = nodo.padre

        return False

    # ==========================
    # MOVER NODOS
    # ==========================

    def mover(self, nodo, destino, lado):

        if nodo is self.raiz:
            return (
                'La raíz no puede convertirse '
                'en hija de otro nodo.'
            )

        if self.es_ancestro(nodo, destino):
            return (
                'No puedes mover un nodo debajo '
                'de sus propios descendientes.'
            )

        if getattr(destino, lado) is not None:
            return (
                'La posición de destino está ocupada.'
            )

        self.guardar_historial()

        padre = nodo.padre

        if padre.izquierdo is nodo:
            padre.izquierdo = None
        else:
            padre.derecho = None

        setattr(destino, lado, nodo)
        nodo.padre = destino

        self.recorrido_texto.set('Recorrido: —')

        self.dibujar()

        return (
            f'Movido «{nodo.valor}» al lado {lado} '
            f'de «{destino.valor}».'
        )

    # ==========================
    # RECORRIDOS DEL ÁRBOL
    # ==========================

    def orden(self, tipo):

        salida = []

        def visita(nodo):

            if nodo is None:
                return

            # PREORDEN
            if tipo == 'Preorden':
                salida.append(nodo)

            visita(nodo.izquierdo)

            # INORDEN
            if tipo == 'Inorden':
                salida.append(nodo)

            visita(nodo.derecho)

            # POSTORDEN
            if tipo == 'Postorden':
                salida.append(nodo)

        visita(self.raiz)

        return salida

    # ==========================
    # ANIMACIÓN DEL RECORRIDO
    # ==========================

    def recorrer(self, tipo):

        self.detener_animacion(
            redibujar=False
        )

        nodos = self.orden(tipo)

        if not nodos:
            self.recorrido_texto.set(
                f'{tipo}: (árbol vacío)'
            )
            self.dibujar()
            return

        self.recorrido_texto.set(f'{tipo}: ')

        self.estado.set(
            'Recorrido animado. Puedes detenerlo.'
        )

        vistos = []

        def avanzar(indice):

            if indice >= len(nodos):

                self.animacion_id = None
                self.resaltado = None

                self.estado.set(
                    f'Recorrido {tipo} terminado.'
                )

                self.dibujar()
                return

            nodo = nodos[indice]

            vistos.append(nodo.valor)

            self.resaltado = nodo

            self.recorrido_texto.set(
                f'{tipo}: ' + ' → '.join(vistos)
            )

            self.dibujar()

            self.animacion_id = self.root.after(
                self.velocidad.get(),
                lambda: avanzar(indice + 1)
            )

        avanzar(0)

    def detener_animacion(self, redibujar=True):

        if self.animacion_id is not None:

            self.root.after_cancel(
                self.animacion_id
            )

            self.animacion_id = None

        self.resaltado = None

        if redibujar:
            self.dibujar()

    # ==========================
    # BUSCAR NODOS
    # ==========================

    def buscar(self):

        objetivo = self.valor.get().strip()

        if not objetivo:

            messagebox.showinfo(
                'Buscar',
                'Escribe el valor que deseas encontrar.'
            )
            return

        coincidencias = [
            n for n in self.orden('Preorden')
            if n.valor == objetivo
        ]

        if coincidencias:

            self.seleccionado = coincidencias[0]

            self.estado.set(
                f'Se encontraron {len(coincidencias)} '
                f'coincidencia(s) de «{objetivo}».'
            )

        else:

            self.seleccionado = None

            self.estado.set(
                f'No existe el valor «{objetivo}».'
            )

        self.dibujar()

    # ==========================
    # ESTADÍSTICAS
    # ==========================

    def estadisticas(self):

        def medir(nodo):

            if nodo is None:
                return 0, 0, 0

            ci, ai, hi = medir(nodo.izquierdo)
            cd, ad, hd = medir(nodo.derecho)

            cantidad = 1 + ci + cd
            altura = 1 + max(ai, ad)

            hoja = (
                1 if (
                    nodo.izquierdo is None
                    and nodo.derecho is None
                )
                else 0
            )

            hojas = hoja + hi + hd

            return cantidad, altura, hojas

        return medir(self.raiz)

    # ==========================
    # VACIAR ÁRBOL
    # ==========================

    def vaciar(self):

        if self.raiz is None:
            return

        confirmar = messagebox.askyesno(
            'Vaciar árbol',
            '¿Eliminar todo el árbol?'
        )

        if not confirmar:
            return

        self.guardar_historial()

        self.raiz = None
        self.seleccionado = None

        self.recorrido_texto.set('Recorrido: —')
        self.estado.set('Árbol vaciado.')

        self.dibujar()

    # ==========================
    # CARGAR ÁRBOL DE EJEMPLO
    # ==========================

    def cargar_ejemplo(self):

        self.guardar_historial()

        self.raiz = Nodo('50')

        self.raiz.izquierdo = Nodo(
            '30', self.raiz
        )

        self.raiz.derecho = Nodo(
            '70', self.raiz
        )

        a = self.raiz.izquierdo
        b = self.raiz.derecho

        a.izquierdo = Nodo('20', a)
        a.derecho = Nodo('40', a)

        b.izquierdo = Nodo('60', b)
        b.derecho = Nodo('80', b)

        self.seleccionado = self.raiz

        self.recorrido_texto.set('Recorrido: —')
        self.estado.set('Ejemplo cargado.')

        self.dibujar()

    # ==========================
    # GUARDAR JSON
    # ==========================

    def guardar(self):

        archivo = filedialog.asksaveasfilename(
            title='Guardar árbol',
            defaultextension='.json',
            filetypes=[
                ('Archivos JSON', '*.json')
            ]
        )

        if not archivo:
            return

        try:

            datos = {
                'tipo': 'arbol_binario',
                'raiz': self.serializar(self.raiz)
            }

            with open(
                archivo,
                'w',
                encoding='utf-8'
            ) as f:

                json.dump(
                    datos,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            self.estado.set(
                f'Árbol guardado en {archivo}.'
            )

        except OSError as error:

            messagebox.showerror(
                'Error al guardar',
                str(error)
            )

    # ==========================
    # ABRIR JSON
    # ==========================

    def abrir(self):

        archivo = filedialog.askopenfilename(
            title='Abrir árbol',
            filetypes=[
                ('Archivos JSON', '*.json')
            ]
        )

        if not archivo:
            return

        try:

            with open(
                archivo,
                'r',
                encoding='utf-8'
            ) as f:

                datos = json.load(f)

            if (
                not isinstance(datos, dict)
                or datos.get('tipo') != 'arbol_binario'
                or 'raiz' not in datos
            ):
                raise ValueError(
                    'El archivo no tiene el formato esperado.'
                )

            nueva_raiz = self.reconstruir(
                datos['raiz']
            )

        except (
            OSError,
            ValueError,
            TypeError,
            RecursionError
        ) as error:

            messagebox.showerror(
                'No se pudo abrir',
                str(error)
            )
            return

        self.guardar_historial()

        self.raiz = nueva_raiz
        self.seleccionado = None

        self.recorrido_texto.set('Recorrido: —')

        self.estado.set(
            f'Árbol cargado desde {archivo}.'
        )

        self.dibujar()

    # ==========================
    # ZOOM
    # ==========================

    def cambiar_zoom(self, diferencia):

        self.escala = max(
            0.55,
            min(
                2.0,
                round(
                    self.escala + diferencia,
                    2
                )
            )
        )

        self.dibujar()

        self.estado.set(
            f'Zoom: {round(self.escala * 100)} %.'
        )

    # ==========================
    # DISTRIBUIR NODOS
    # ==========================

    def distribuir(self):

        self.posiciones.clear()

        lista = []

        def inorden(nodo, nivel):

            if nodo is None:
                return

            inorden(
                nodo.izquierdo,
                nivel + 1
            )

            lista.append(
                (nodo, nivel)
            )

            inorden(
                nodo.derecho,
                nivel + 1
            )

        inorden(self.raiz, 0)

        sep_x = 90 * self.escala
        sep_y = 112 * self.escala

        ancho = max(
            self.canvas.winfo_width(),
            (len(lista) + 1) * sep_x + 100
        )

        profundidad = max(
            (nivel for _, nivel in lista),
            default=0
        )

        alto = max(
            self.canvas.winfo_height(),
            160 + (profundidad + 1) * sep_y
        )

        if lista:

            inicio = (
                ancho - (len(lista) - 1) * sep_x
            ) / 2

        else:
            inicio = ancho / 2

        for i, (nodo, nivel) in enumerate(lista):

            x = inicio + i * sep_x
            y = 72 + nivel * sep_y

            self.posiciones[nodo] = (x, y)

        return ancho, alto

    # ==========================
    # DIBUJAR ÁRBOL
    # ==========================

    def dibujar(self):

        self.canvas.delete('all')

        ancho, alto = self.distribuir()

        self.canvas.configure(
            scrollregion=(0, 0, ancho, alto)
        )

        total, altura, hojas = self.estadisticas()

        seleccionado = (
            self.seleccionado.valor
            if self.seleccionado
            else 'ninguno'
        )

        self.info.set(
            f'Nodos: {total} | '
            f'Altura: {altura} niveles | '
            f'Hojas: {hojas} | '
            f'Seleccionado: {seleccionado}'
        )

        if self.raiz is None:

            self.canvas.create_text(
                ancho / 2,
                130,
                text='Árbol vacío: agrega una raíz o carga un ejemplo',
                fill=MUTED,
                font=('DejaVu Sans', 15, 'bold')
            )
            return

        radio = 22 * self.escala

        # Dibujar conexiones
        for nodo, (x, y) in self.posiciones.items():

            for hijo in (
                nodo.izquierdo,
                nodo.derecho
            ):

                if hijo:

                    hx, hy = self.posiciones[hijo]

                    self.canvas.create_line(
                        x, y,
                        hx, hy,
                        fill=EDGE,
                        width=2
                    )

        # Dibujar círculos
        for nodo, (x, y) in self.posiciones.items():

            if nodo is self.resaltado:
                color = YELLOW

            elif nodo is self.seleccionado:
                color = GREEN

            else:
                color = BLUE

            self.canvas.create_oval(
                x - radio,
                y - radio,
                x + radio,
                y + radio,
                fill=color,
                outline=(
                    '#e5edff'
                    if nodo is self.seleccionado
                    else color
                ),
                width=2
            )

            valor = nodo.valor

            if len(valor) > 7:
                valor = valor[:6] + '…'

            self.canvas.create_text(
                x, y,
                text=valor,
                fill='#101827',
                font=(
                    'DejaVu Sans',
                    max(8, int(10 * self.escala)),
                    'bold'
                )
            )

        # Resaltar destino del movimiento
        if (
            self.destino_drag
            and self.destino_drag in self.posiciones
        ):

            x, y = self.posiciones[
                self.destino_drag
            ]

            dx = (
                -radio * 0.65
                if self.lado_drag == 'izquierdo'
                else radio * 0.65
            )

            self.canvas.create_oval(
                x + dx - 10,
                y - radio - 14,
                x + dx + 10,
                y - radio + 6,
                outline=YELLOW,
                width=3
            )

    # ==========================
    # DETECTAR NODO CON EL MOUSE
    # ==========================

    def nodo_en(self, x, y):

        radio = (27 * self.escala) ** 2

        for nodo, (nx, ny) in self.posiciones.items():

            distancia = (
                (x - nx) ** 2
                + (y - ny) ** 2
            )

            if distancia <= radio:
                return nodo

        return None

    # ==========================
    # MOUSE: PRESIONAR
    # ==========================

    def mouse_abajo(self, event):

        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        self.origen_drag = self.nodo_en(x, y)

        self.inicio_drag = (x, y)

        self.arrastrando = False
        self.destino_drag = None
        self.lado_drag = None

        self.seleccionado = self.origen_drag

        if self.seleccionado:

            self.estado.set(
                f'Seleccionado «{self.seleccionado.valor}». '
                'Arrástralo sobre otro nodo para mover su rama.'
            )

        self.dibujar()

    # ==========================
    # MOUSE: ARRASTRAR
    # ==========================

    def mouse_mover(self, event):

        if self.origen_drag is None:
            return

        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        distancia = (
            (x - self.inicio_drag[0]) ** 2
            + (y - self.inicio_drag[1]) ** 2
        )

        if distancia > 81:
            self.arrastrando = True

        if self.arrastrando:

            destino = self.nodo_en(x, y)

            if destino is not self.origen_drag:
                self.destino_drag = destino
            else:
                self.destino_drag = None

            if self.destino_drag:

                tx, _ = self.posiciones[
                    self.destino_drag
                ]

                self.lado_drag = (
                    'izquierdo'
                    if x < tx
                    else 'derecho'
                )

            else:
                self.lado_drag = None

            self.dibujar()

    # ==========================
    # MOUSE: SOLTAR
    # ==========================

    def mouse_arriba(self, event):

        if self.origen_drag is None:
            return

        origen = self.origen_drag

        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        destino = self.nodo_en(x, y)

        movido = self.arrastrando

        self.origen_drag = None
        self.inicio_drag = None
        self.arrastrando = False
        self.destino_drag = None
        self.lado_drag = None

        if (
            movido
            and destino is not None
            and destino is not origen
        ):

            tx, _ = self.posiciones[destino]

            lado = (
                'izquierdo'
                if x < tx
                else 'derecho'
            )

            mensaje = self.mover(
                origen,
                destino,
                lado
            )

            self.estado.set(mensaje)

        elif movido:

            self.estado.set(
                'Movimiento cancelado: '
                'suelta el nodo encima de otro nodo.'
            )

        self.dibujar()

    # ==========================
    # EXPORTAR IMAGEN SVG
    # ==========================

    def exportar_svg(self):

        if self.raiz is None:

            messagebox.showinfo(
                'Árbol vacío',
                'Primero crea o carga un árbol.'
            )
            return

        archivo = filedialog.asksaveasfilename(
            title='Exportar dibujo',
            defaultextension='.svg',
            filetypes=[
                ('Imagen SVG', '*.svg')
            ]
        )

        if not archivo:
            return

        ancho, alto = self.distribuir()

        partes = [
            (
                f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'width="{int(ancho)}" '
                f'height="{int(alto)}" '
                f'viewBox="0 0 {int(ancho)} {int(alto)}">'
            ),
            (
                f'<rect width="100%" height="100%" '
                f'fill="{CANVAS_BG}"/>'
            )
        ]

        # Líneas
        for nodo, (x, y) in self.posiciones.items():

            for hijo in (
                nodo.izquierdo,
                nodo.derecho
            ):

                if hijo:

                    hx, hy = self.posiciones[hijo]

                    partes.append(
                        f'<line '
                        f'x1="{x:.1f}" y1="{y:.1f}" '
                        f'x2="{hx:.1f}" y2="{hy:.1f}" '
                        f'stroke="{EDGE}" '
                        f'stroke-width="2"/>'
                    )

        # Nodos
        for nodo, (x, y) in self.posiciones.items():

            color = (
                GREEN
                if nodo is self.seleccionado
                else BLUE
            )

            partes.append(
                f'<circle '
                f'cx="{x:.1f}" '
                f'cy="{y:.1f}" '
                f'r="{22 * self.escala:.1f}" '
                f'fill="{color}"/>'
            )

            texto = escape(nodo.valor)

            partes.append(
                f'<text '
                f'x="{x:.1f}" '
                f'y="{y + 4:.1f}" '
                f'font-size="{max(9, int(11 * self.escala))}" '
                f'font-family="sans-serif" '
                f'font-weight="bold" '
                f'text-anchor="middle" '
                f'fill="#101827">{texto}</text>'
            )

        partes.append('</svg>')

        try:

            with open(
                archivo,
                'w',
                encoding='utf-8'
            ) as f:

                f.write('\n'.join(partes))

            self.estado.set(
                f'Imagen exportada: {archivo}.'
            )

        except OSError as error:

            messagebox.showerror(
                'Error',
                str(error)
            )


# ==========================
# INICIAR PROGRAMA
# ==========================

if __name__ == '__main__':

    ventana = tk.Tk()

    ArbolApp(ventana)

    ventana.mainloop()
