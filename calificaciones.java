import java.util.Random;
import java.util.Scanner;

public class calificaciones {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random rnd = new Random();

        // 10,000 materias fijas como columnas
        final int TOTAL_MATERIAS = 10_000;

        System.out.println("==========================================================================");
        System.out.println("  SISTEMA DE CALIFICACIONES: FILAS = ALUMNOS | COLUMNAS = 10,000 MATERIAS ");
        System.out.println("==========================================================================");

        // 1. Entrada del número de alumnos
        System.out.print("Ingrese la cantidad de alumnos (ej. 500, 1000, 10000): ");
        int totalAlumnos = scanner.nextInt();

        System.out.println("\nReservando memoria y generando calificaciones aleatorias...");

        // Forma B: [Alumnos][Materias] (N filas x 10,000 columnas)
        double[][] matrizAluMat = new double[totalAlumnos][TOTAL_MATERIAS];
        // Forma A: [Materias][Alumnos] (10,000 filas x N columnas)
        double[][] matrizMatAlu = new double[TOTAL_MATERIAS][totalAlumnos];

        for (int a = 0; a < totalAlumnos; a++) {
            for (int m = 0; m < TOTAL_MATERIAS; m++) {
                double calif = Math.round((50.0 + rnd.nextDouble() * 50.0) * 10.0) / 10.0;
                matrizAluMat[a][m] = calif;
                matrizMatAlu[m][a] = calif;
            }
        }
        System.out.println("Datos cargados exitosamente.\n");

        // 2. Opción de visualización de filas
        System.out.print("¿Cuántas filas de alumnos desea visualizar en la tabla? (ej. 5, 10, 20): ");
        int filasVer = scanner.nextInt();
        int filasAMostrar = Math.min(filasVer, totalAlumnos);

        // --------------------------------------------------------------------------
        // DIBUJO DE LA TABLA: ALUMNOS (FILAS) x 10,000 MATERIAS (COLUMNAS)
        // Muestra: Mat 1 a 4 ... Mat 9999 y Mat 10000
        // --------------------------------------------------------------------------
        System.out.println("\n+---------------+------------+------------+------------+------------+-------+------------+------------+");
        System.out.printf("| %-13s | %-10s | %-10s | %-10s | %-10s | %-5s | %-10s | %-10s |%n", 
                "Alumno", "Materia 1", "Materia 2", "Materia 3", "Materia 4", "...", "Mat 9999", "Mat 10000");
        System.out.println("+---------------+------------+------------+------------+------------+-------+------------+------------+");

        for (int a = 0; a < filasAMostrar; a++) {
            System.out.printf("| Alumno %-6d |", (a + 1));
            // Primeras 4 materias
            for (int m = 0; m < 4; m++) {
                System.out.printf("   %5.1f    |", matrizAluMat[a][m]);
            }
            System.out.print("  ...  |");
            // Últimas 2 materias (9999 y 10000)
            for (int m = TOTAL_MATERIAS - 2; m < TOTAL_MATERIAS; m++) {
                System.out.printf("   %5.1f    |", matrizAluMat[a][m]);
            }
            System.out.println();
        }

        if (filasAMostrar < totalAlumnos) {
            System.out.println("| ...           |    ...     |    ...     |    ...     |    ...     |  ...  |    ...     |    ...     |");
            System.out.printf("| Alumno %-6d |", totalAlumnos);
            for (int m = 0; m < 4; m++) {
                System.out.printf("   %5.1f    |", matrizAluMat[totalAlumnos - 1][m]);
            }
            System.out.print("  ...  |");
            for (int m = TOTAL_MATERIAS - 2; m < TOTAL_MATERIAS; m++) {
                System.out.printf("   %5.1f    |", matrizAluMat[totalAlumnos - 1][m]);
            }
            System.out.println();
        }
        System.out.println("+---------------+------------+------------+------------+------------+-------+------------+------------+");

        // 3. Consulta específica (Scanner)
        System.out.printf("%nIngrese el número de alumno a consultar (1 a %d): ", totalAlumnos);
        int numAlumno = scanner.nextInt();

        System.out.printf("Ingrese el número de materia a consultar (1 a %,d): ", TOTAL_MATERIAS);
        int numMateria = scanner.nextInt();

        int idxAlumno = numAlumno - 1;
        int idxMateria = numMateria - 1;

        if (idxAlumno < 0 || idxAlumno >= totalAlumnos || idxMateria < 0 || idxMateria >= TOTAL_MATERIAS) {
            System.out.println("Error: Índices fuera de rango.");
            scanner.close();
            return;
        }

        // 4. Medición de búsqueda puntual (10 millones de lecturas O(1))
        final int REPETICIONES = 10_000_000;
        long tInicio = System.nanoTime();
        double califB = 0;
        for (int i = 0; i < REPETICIONES; i++) {
            califB = matrizAluMat[idxAlumno][idxMateria]; // [Alumno][Materia]
        }
        long tFin = System.nanoTime();
        double tAccesoAluMat = (tFin - tInicio) / 1_000_000.0;

        tInicio = System.nanoTime();
        double califA = 0;
        for (int i = 0; i < REPETICIONES; i++) {
            califA = matrizMatAlu[idxMateria][idxAlumno]; // [Materia][Alumno]
        }
        tFin = System.nanoTime();
        double tAccesoMatAlu = (tFin - tInicio) / 1_000_000.0;

        // 5. Medición de recorrido secuencial completo
        // Recorrido Forma B: [Alumnos][Materias] -> Fila continua de 10,000 doubles
        tInicio = System.nanoTime();
        double sumB = 0;
        for (int a = 0; a < totalAlumnos; a++) {
            for (int m = 0; m < TOTAL_MATERIAS; m++) {
                sumB += matrizAluMat[a][m];
            }
        }
        tFin = System.nanoTime();
        double tRecorridoAluMat = (tFin - tInicio) / 1_000_000.0;

        // Recorrido Forma A: [Materias][Alumnos] -> 10,000 arreglos
        tInicio = System.nanoTime();
        double sumA = 0;
        for (int m = 0; m < TOTAL_MATERIAS; m++) {
            for (int a = 0; a < totalAlumnos; a++) {
                sumA += matrizMatAlu[m][a];
            }
        }
        tFin = System.nanoTime();
        double tRecorridoMatAlu = (tFin - tInicio) / 1_000_000.0;

        // 6. Tabla comparativa de resultados
        System.out.println("\n+-----------------------------------------------------------------------------------+");
        System.out.printf("| CALIFICACIÓN CONSULTADA: Alumno %-6d | Materia %-5d | Nota: %5.1f              |%n",
                numAlumno, numMateria, califB);
        System.out.println("+-----------------------------------------------------------------------------------+");
        System.out.println("|                      TABLA COMPARATIVA DE RENDIMIENTO                             |");
        System.out.println("+-----------------------------------+-----------------------+-----------------------+");
        System.out.printf("| %-33s | %-21s | %-21s |%n", "Operación", "[Alumno][Materia]", "[Materia][Alumno]");
        System.out.printf("| %-33s | %-21s | %-21s |%n", "", "(N x 10,000)", "(10,000 x N)");
        System.out.println("+-----------------------------------+-----------------------+-----------------------+");
        System.out.printf("| Búsqueda Puntual (10M veces)      | %17.3f ms | %17.3f ms |%n", tAccesoAluMat, tAccesoMatAlu);
        System.out.printf("| Recorrido Completo de la Matriz   | %17.3f ms | %17.3f ms |%n", tRecorridoAluMat, tRecorridoMatAlu);
        System.out.println("+-----------------------------------+-----------------------+-----------------------+");

        scanner.close();
    }
}