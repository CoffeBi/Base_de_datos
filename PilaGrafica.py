import tkinter as tk
from tkinter import messagebox

class PilaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Pila (Stack) - Estructuras de Datos")
        self.root.geometry("500x630")
        self.root.config(bg="#121212")  # Fondo negro/oscuro
        
        self.pila = []
        self.capacidad_maxima = 8  # Límite visual de elementos
        
        # Registrar función de validación de entradas (solo números)
        vcmd = (self.root.register(self.validar_numero), '%P')
        
        # Título
        titulo = tk.Label(
            root, 
            text="Simulación Gráfica de una Pila", 
            font=("Arial", 16, "bold"), 
            bg="#121212", 
            fg="#ffffff"
        )
        titulo.pack(pady=15)
        
        # Frame de Controles (Entrada y Botones)
        control_frame = tk.Frame(root, bg="#121212")
        control_frame.pack(pady=10)
        
        # Campo de entrada restringido a solo números
        self.entrada_val = tk.Entry(
            control_frame, 
            font=("Arial", 14), 
            width=12, 
            bg="#2a2a2a", 
            fg="#ffffff", 
            insertbackground="white",
            validate="key", 
            validatecommand=vcmd
        )
        self.entrada_val.grid(row=0, column=0, padx=5)
        self.entrada_val.bind("<Return>", lambda event: self.push())
        
        # Botones estilo Morado / Negro / Blanco
        btn_push = tk.Button(
            control_frame, text="Apilar (Push)", font=("Arial", 10, "bold"), 
            bg="#7b1fa2", fg="#ffffff", activebackground="#9c27b0", activeforeground="#ffffff",
            width=12, command=self.push, bd=0, cursor="hand2"
        )
        btn_push.grid(row=0, column=1, padx=5)
        
        btn_pop = tk.Button(
            control_frame, text="Desapilar (Pop)", font=("Arial", 10, "bold"), 
            bg="#4a148c", fg="#ffffff", activebackground="#6a1b9a", activeforeground="#ffffff",
            width=12, command=self.pop, bd=0, cursor="hand2"
        )
        btn_pop.grid(row=1, column=0, padx=5, pady=8)
        
        btn_peek = tk.Button(
            control_frame, text="Cima (Peek)", font=("Arial", 10, "bold"), 
            bg="#ab47bc", fg="#ffffff", activebackground="#ba68c8", activeforeground="#ffffff",
            width=12, command=self.peek, bd=0, cursor="hand2"
        )
        btn_peek.grid(row=1, column=1, padx=5, pady=8)
        
        # Canvas para la representación gráfica de la pila
        self.canvas_frame = tk.Frame(root, bg="#ab47bc", bd=2)
        self.canvas_frame.pack(pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=260, height=320, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack()
        
        # Base de la pila (Líneas moradas)
        self.canvas.create_line(30, 300, 230, 300, fill="#ab47bc", width=4)
        self.canvas.create_line(30, 50, 30, 300, fill="#ab47bc", width=4)
        self.canvas.create_line(230, 50, 230, 300, fill="#ab47bc", width=4)
        
        # Etiqueta de estado
        self.lbl_estado = tk.Label(root, text="Estado: Pila Vacía", font=("Arial", 11, "italic"), bg="#121212", fg="#ce93d8")
        self.lbl_estado.pack(pady=5)
        
        self.actualizar_visualizacion()

    def validar_numero(self, texto):
        """ Valida que el texto ingresado sea exclusivamente numérico """
        if texto == "" or texto == "-":
            return True
        try:
            float(texto)
            return True
        except ValueError:
            return False

    def push(self):
        valor = self.entrada_val.get().strip()
        if not valor or valor == "-":
            messagebox.showwarning("Advertencia", "Por favor ingresa un número válido.")
            return
        
        if len(self.pila) >= self.capacidad_maxima:
            messagebox.showerror("Desbordamiento", "¡La pila está llena (Overflow)! No caben más elementos.")
            return
            
        self.pila.append(valor)
        self.entrada_val.delete(0, tk.END)
        self.actualizar_visualizacion()

    def pop(self):
        if not self.pila:
            messagebox.showerror("Subdesbordamiento", "¡La pila está vacía (Underflow)! No hay elementos para desapilar.")
            return
            
        eliminado = self.pila.pop()
        messagebox.showinfo("Elemento Removido", f"Se ha desapilado el número: {eliminado}")
        self.actualizar_visualizacion()

    def peek(self):
        if not self.pila:
            messagebox.showinfo("Cima (Peek)", "La pila está vacía.")
        else:
            messagebox.showinfo("Cima (Peek)", f"El número en la cima es: {self.pila[-1]}")

    def actualizar_visualizacion(self):
        # Limpiar elementos dibujados anteriormente
        self.canvas.delete("bloque")
        self.canvas.delete("texto")
        self.canvas.delete("tope_lbl")
        
        y_inicial = 280
        altura_bloque = 30
        ancho_bloque = 190
        x1 = 35
        x2 = x1 + ancho_bloque
        
        for i, elemento in enumerate(self.pila):
            y2 = y_inicial - (i * (altura_bloque + 5))
            y1 = y2 - altura_bloque
            
            # Color morado oscuro para los bloques inferiores y morado brillante para la cima
            es_cima = (i == len(self.pila) - 1)
            color_bloque = "#8e24aa" if es_cima else "#4a148c"
            color_borde = "#e1bee7" if es_cima else "#7b1fa2"
            
            # Dibujar rectángulo del elemento
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color_bloque, outline=color_borde, width=2, tags="bloque")
            
            # Texto blanco en el centro
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(elemento), fill="#ffffff", font=("Arial", 11, "bold"), tags="texto")
            
        # Señalar la Cima (Top)
        if self.pila:
            y_cima = y_inicial - ((len(self.pila) - 1) * (altura_bloque + 5)) - (altura_bloque / 2)
            self.canvas.create_text(235, y_cima, text="← Cima", anchor="w", fill="#e1bee7", font=("Arial", 10, "bold"), tags="tope_lbl")
            self.lbl_estado.config(text=f"Elementos en la pila: {len(self.pila)} | Cima: {self.pila[-1]}")
        else:
            self.lbl_estado.config(text="Estado: Pila Vacía")

if __name__ == "__main__":
    root = tk.Tk()
    app = PilaApp(root)
    root.mainloop()