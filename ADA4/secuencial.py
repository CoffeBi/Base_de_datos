def busqueda_secuencial(alumnos, objetivo):
    comparaciones = 0

    for i in range(len(alumnos)):
        comparaciones += 1

        if alumnos[i].casefold() == objetivo.casefold():
            return i, comparaciones

    return -1, comparaciones