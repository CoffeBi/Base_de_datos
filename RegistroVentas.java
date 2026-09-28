import java.util.Scanner;

public class RegistroVentas {
    // Arreglo bidimensional: 12 meses (filas) x 3 departamentos (columnas)
    private double[][] ventas;
    private String[] meses = {"Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"};
    private String[] departamentos = {"Ropa", "Deportes", "Juguetería"};

    public RegistroVentas() {
        ventas = new double[12][3];
    }

    // 1. Método para insertar elementos en el arreglo
    public void insertarVenta(int mes, int departamento, double monto) {
        if (mes >= 0 && mes < 12 && departamento >= 0 && departamento < 3) {
            ventas[mes][departamento] = monto;
            System.out.println("-> Venta insertada correctamente.");
        } else {
            System.out.println("-> Error: Índices de mes o departamento inválidos.");
        }
    }

    // 2. Método para buscar algún elemento en particular (por monto exacto)
    public void buscarVenta(double monto) {
        boolean encontrado = false;
        for (int i = 0; i < 12; i++) {
            for (int j = 0; j < 3; j++) {
                if (ventas[i][j] == monto) {
                    System.out.println("-> Elemento de $" + monto + " encontrado en el mes de " + meses[i] + ", departamento de " + departamentos[j] + ".");
                    encontrado = true;
                }
            }
        }
        if (!encontrado) {
            System.out.println("-> No se encontró ninguna venta con el monto especificado.");
        }
    }

    // 3. Método para eliminar una venta en particular (restableciendo a 0.0)
    public void eliminarVenta(int mes, int departamento) {
        if (mes >= 0 && mes < 12 && departamento >= 0 && departamento < 3) {
            ventas[mes][departamento] = 0.0;
            System.out.println("-> Venta del mes " + meses[mes] + " en " + departamentos[departamento] + " ha sido eliminada.");
        } else {
            System.out.println("-> Error: Índices de mes o departamento inválidos.");
        }
    }

    // MÉTODO PRINCIPAL CON MENÚ INTERACTIVO
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        RegistroVentas registro = new RegistroVentas();
        int opcion = 0;

        System.out.println("=========================================");
        System.out.println("   SISTEMA DE REGISTRO DE VENTAS");
        System.out.println("=========================================");

        do {
            System.out.println("\n¿Qué deseas hacer?");
            System.out.println("1. Insertar una venta");
            System.out.println("2. Buscar una venta (por monto)");
            System.out.println("3. Eliminar una venta");
            System.out.println("4. Salir");
            System.out.print("Elige una opción (1-4): ");
            
            opcion = scanner.nextInt();

            switch (opcion) {
                case 1:
                    System.out.print("Ingresa el mes (0 = Enero, 11 = Diciembre): ");
                    int mesIns = scanner.nextInt();
                    System.out.print("Ingresa el departamento (0 = Ropa, 1 = Deportes, 2 = Juguetería): ");
                    int depIns = scanner.nextInt();
                    System.out.print("Ingresa el monto de la venta: ");
                    double montoIns = scanner.nextDouble();
                    registro.insertarVenta(mesIns, depIns, montoIns);
                    break;
                    
                case 2:
                    System.out.print("Ingresa el monto exacto a buscar: ");
                    double montoBusq = scanner.nextDouble();
                    registro.buscarVenta(montoBusq);
                    break;
                    
                case 3:
                    System.out.print("Ingresa el mes de la venta a eliminar (0 = Enero, 11 = Diciembre): ");
                    int mesEli = scanner.nextInt();
                    System.out.print("Ingresa el departamento (0 = Ropa, 1 = Deportes, 2 = Juguetería): ");
                    int depEli = scanner.nextInt();
                    registro.eliminarVenta(mesEli, depEli);
                    break;
                    
                case 4:
                    System.out.println("Saliendo del sistema. ¡Hasta luego!");
                    break;
                    
                default:
                    System.out.println("-> Opción no válida. Intenta de nuevo.");
            }
        } while (opcion != 4);

        scanner.close();
    }
}