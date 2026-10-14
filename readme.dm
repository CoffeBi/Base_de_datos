# Torre de Hanoi en Python
En este ejercicio de programacion veremos a **Torre de Hanoi**,en el cual nos pide que cumpla con los requisitos de análisis de métodos, medición de tiempos de ejecución para $5$, $10$, $30$ y $64$ discos, y sus respectivas conclusiones de cada uno.

---

## Descripción de Métodos

El programa se encuentra estructurado utilizando **2 métodos** principales:

1. **`torre_hanoi(n, origen, destino, auxiliar)`**
   * **Tipo**: Método recursivo principal.
   Propósito: Nos ayuda a implementa la estrategia de "divide y vencerás" para calcular los movimientos necesarios al trasladar $n$ cantidad de discos desde el poste de origen hasta su destino, apoyándose en una torre auxiliar,Su complejidad temporal es de orden exponencial $O(2^n)$.

2. **`medir_tiempo_hanoi(discos)`**
   * **Tipo**: Método auxiliar de rendimiento.
   * **Propósito**: Es el encargado de coordinar la ejecución del algoritmo midiendo con alta precisión  (`time.perf_counter`) el tiempo transcurrido en segundos que le toma al sistema procesar cada uno de los discos.
---

## Ejecución y Medición de Tiempos ($5, 10, 30$ y $64$ discos)

Dado que la fórmula matemática para calcular el número total de movimientos es $2^n - 1$, el comportamiento del algoritmo es estrictamente exponencial:

| Discos ($n$) | Número de Movimientos ($2^n - 1$) | Tiempo de Ejecución / Estimación |
| :---: | :--- | :--- |
| **5** | 31 | $\approx 0.000009$ segundos (Medido) |
| **10** | 1,023 | $\approx 0.000083$ segundos (Medido) |
| **30** | 1,073,741,823 | $\approx 2$ a $5$ minutos (Cálculo teórico por saturación de pila) |
| **64** | 18,446,744,073,709,551,615 | $\approx 584$ mil millones de años (Cálculo teórico puro) |

---

## Conclusiones

## Conclusiones

1. **Impacto del crecimiento exponencial ($O(2^n)$):** En la práctica se observa cómo al aumentar unos pocos discos, la cantidad de operaciones se multiplica drásticamente. Mover 5 o 10 discos toma una fracción de segundo, pero llegar a 30 discos ya implica más de mil millones de movimientos.

2. **Límites de la computadora y del programa:** Intentar ejecutar el algoritmo recursivo para 30 o 64 discos de manera real provocaría que el programa se trabe por minutos o incluso años, además de saturar la memoria por tantas llamadas a la función. Por ello, fue necesario incluir una validación para calcular los movimientos directamente con la fórmula ($2^n - 1$) en los casos muy grandes.

3. **Uso de la recursividad:** La solución recursiva resulta muy práctica y limpia de programar para aplicar la estrategia de "divide y vencerás". Sin embargo, nos demuestra que no todos los problemas recursivos son escalables para grandes volúmenes de datos debido al alto costo de procesamiento que requieren.

___

# Sistema de Registro de Ventas - Java y Python

## Descripción
Este es un programa creado con fines educativos para visualizar el almacenamiento de datos. En este código se utiliza una estructura de datos de matriz bidimensional para organizar la información del ejercicio solicitado.

Específicamente, el sistema organiza los datos en un arreglo de 12 filas y 3 columnas:
- **Filas (12):** Representan los meses del año (de Enero a Diciembre).
- **Columnas (3):** Representan los departamentos de la tienda: **Ropa**, **Deportes** y **Juguetería**.

El usuario puede interactuar con el sistema a través de un menú cíclico que se mantiene en ejecución hasta decidir salir.

## Funciones Principales
1. **Insertar una venta:** Permite registrar un monto exacto de venta en un mes y departamento específico.
2. **Buscar una venta:** Realiza una búsqueda secuencial en toda la matriz para encontrar un monto exacto y, si existe, devuelve el mes y el departamento donde se encontró.
3. **Eliminar una venta:** Permite limpiar el registro de un mes y departamento específico (restableciendo el valor en la matriz a `0.0`).

## Requisitos Previos
- Tener instalado **Java Development Kit (JDK)** (versión 8 o superior) o **Python 3**.
- Una terminal o consola de comandos, o un entorno de desarrollo (IDE) como VS Code, Eclipse, IntelliJ IDEA o un entorno en línea como OnlineGDB.

## Compilación y Ejecución

### Java
1. Abre tu terminal y navega hasta la carpeta donde guardaste el archivo `RegistroVentas.java`.
2. Compila el código fuente:
   ```bash
   javac RegistroVentas.java
   ```
3. Ejecuta el programa:
   ```bash
   java RegistroVentas
   ```

### Python
1. Abre tu terminal y navega hasta la carpeta donde guardaste el archivo `registro_ventas.py`.
2. Ejecuta el programa:
   ```bash
   python registro_ventas.py
   ```