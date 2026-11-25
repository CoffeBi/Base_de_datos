def busqueda_binaria(matriculas, objetivo):
    inicio = 0
    fin = len(matriculas) - 1
    comparaciones = 0

    while inicio <= fin:
        medio = (inicio + fin) // 2
        comparaciones += 1

        if matriculas[medio] == objetivo:
            return medio, comparaciones

        elif matriculas[medio] < objetivo:
            inicio = medio + 1

        else:
            fin = medio - 1

    return -1, comparaciones