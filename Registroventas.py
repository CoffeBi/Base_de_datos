class RegistroVentas:
    def __init__(self):
        # Generar arreglo bidimensional de 12 filas (meses) x 3 columnas (departamentos) inicializado en 0.0
        self.ventas = [[0.0 for _ in range(3)] for _ in range(12)]
        self.meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.departamentos = ["Ropa", "Deportes", "Juguetería"]

    # 1. Método para insertar elementos en el arreglo
    def insertar_venta(self, mes, departamento, monto):
        if 0 <= mes < 12 and 0 <= departamento < 3:
            self.ventas[mes][departamento] = monto
            print("-> Venta insertada correctamente.")
        else:
            print("-> Error: Índices de mes o departamento inválidos.")

    # 2. Método para buscar algún elemento en particular (por monto exacto)
    def buscar_venta(self, monto):
        encontrado = False
        for i in range(12):
            for j in range(3):
                if self.ventas[i][j] == monto:
                    print(f"-> Elemento de ${monto} encontrado en el mes de {self.meses[i]}, departamento de {self.departamentos[j]}.")
                    encontrado = True
        
        if not encontrado:
            print("-> No se encontró ninguna venta con el monto especificado.")

    # 3. Método para eliminar una venta en particular
    def eliminar_venta(self, mes, departamento):
        if 0 <= mes < 12 and 0 <= departamento < 3:
            self.ventas[mes][departamento] = 0.0
            print(f"-> Venta del mes {self.meses[mes]} en {self.departamentos[departamento]} ha sido eliminada.")
        else:
            print("-> Error: Índices de mes o departamento inválidos.")


# FUNCION PRINCIPAL CON MENÚ INTERACTIVO
def main():
    registro = RegistroVentas()
    
    print("=========================================")
    print("   SISTEMA DE REGISTRO DE VENTAS")
    print("=========================================")

    while True:
        print("\n¿Qué deseas hacer?")
        print("1. Insertar una venta")
        print("2. Buscar una venta (por monto)")
        print("3. Eliminar una venta")
        print("4. Salir")
        
        opcion = input("Elige una opción (1-4): ")

        if opcion == '1':
            try:
                mes_ins = int(input("Ingresa el mes (0 = Enero, 11 = Diciembre): "))
                dep_ins = int(input("Ingresa el departamento (0 = Ropa, 1 = Deportes, 2 = Juguetería): "))
                monto_ins = float(input("Ingresa el monto de la venta: "))
                registro.insertar_venta(mes_ins, dep_ins, monto_ins)
            except ValueError:
                print("-> Error: Por favor ingresa valores numéricos válidos.")

        elif opcion == '2':
            try:
                monto_busq = float(input("Ingresa el monto exacto a buscar: "))
                registro.buscar_venta(monto_busq)
            except ValueError:
                print("-> Error: Por favor ingresa un monto numérico válido.")

        elif opcion == '3':
            try:
                mes_eli = int(input("Ingresa el mes de la venta a eliminar (0 = Enero, 11 = Diciembre): "))
                dep_eli = int(input("Ingresa el departamento (0 = Ropa, 1 = Deportes, 2 = Juguetería): "))
                registro.eliminar_venta(mes_eli, dep_eli)
            except ValueError:
                print("-> Error: Por favor ingresa valores numéricos válidos.")

        elif opcion == '4':
            print("Saliendo del sistema. ¡Hasta luego!")
            break
            
        else:
            print("-> Opción no válida. Intenta de nuevo.")

# Ejecutar el programa
if __name__ == "__main__":
    main()