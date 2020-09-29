import os
import array
from concurrent import futures


def hilos(size, sizefile):
    # seteo un valor minimo para la creacion de la cant de hilos
    if size < 10000:
        size = 10000
    if size % 3 != 0:
        size += (3 - (size % 3))
    cant_hilos = round((sizefile / size) + 0.5)
    return cant_hilos, size


def calcular_posicion(imagen):
    for i in range(imagen.count(b"\n# ")):  # Si hay comentarios en la imagen
        barra_n_numeral = imagen.find(b"\n#")+1
        barra_n = imagen.find(b"\n", barra_n_numeral)
        # Ultimo barra antes de arrancar con la imagen
    if imagen.count(b"\n# ") == 0:  # Si no hay comentarios
        barra_n = imagen.find(b"\n")
    medidas = imagen.find(b"\n", barra_n + 1)
    profundidad = imagen.find(b"\n", medidas+1)
    return profundidad + 1


def procesar(cant_hilos, size, files, color, intensidad):
    # abro la imagen
    archivo = os.open(files, os.O_RDONLY)
    # abro la imagen y lo guardo en imagen
    imagen = os.read(archivo, size)
    # calculo la posicion donde comienza el cuerpo de la imagen
    posicion = calcular_posicion(imagen)
    encabezado = imagen[:posicion]
    encabezado = [i for i in encabezado]
    # Me paro donde inicia el curpo en la imagen
    os.lseek(archivo, posicion, 0)
    body = ""
    # aca almaceno el bloque leido
    lista = []
    # aca almaceno las instancias de los hilos
    lista2 = []
    # escribo la cabecera
    cuerpo = array.array('B', encabezado)
    # hacer con for y la cantidad de hilos
    hilos = futures.ThreadPoolExecutor(max_workers=cant_hilos)
    for i in range(cant_hilos):
        body = os.read(archivo, size)
        lista = [i for i in body]
        if color == "rojo":
            lista2.append(hilos.submit(filtro_rojo, lista, intensidad))
        elif color == "verde":
            lista2.append(hilos.submit(filtro_verde, lista, intensidad))
        elif color == "azul":
            lista2.append(hilos.submit(filtro_blue, lista, intensidad))
        elif color == "bw":
            lista2.append(hilos.submit(filtro_bw, lista, intensidad))
    for i in lista2:
        cuerpo += array.array('B', i.result())
    os.close(archivo)
    return cuerpo


def filtro_rojo(lista, intensidad):
    for i in range(0, len(lista) - 3, 3):
        lista[i] = round((lista[i]) * (intensidad))
        if lista[i] > 255:
            lista[i] = 255
        lista[i + 1] = 0
        lista[i + 2] = 0
    return lista


def filtro_verde(lista, intensidad):
    for i in range(0, (len(lista) - 3), 3):
        lista[i] = 0
        lista[i + 1] = round(lista[i + 1] * intensidad)
        if lista[i + 1] > 255:
            lista[i + 1] = 255
        lista[i + 2] = 0
    return lista


def filtro_blue(lista, intensidad):
    for i in range(0, len(lista) - 3, 3):
        lista[i] = 0
        lista[i + 1] = 0
        lista[i + 2] = round(float(lista[i + 2]) * intensidad)
        if lista[i + 2] > 255:
            lista[i + 2] = 255
    return lista


def filtro_bw(lista, intensidad):
    for i in range(0, len(lista) - 3, 3):
        pixel_bw = round((lista[i] + lista[i + 1] + lista[i + 2])/3)
        pixel_bw = round(pixel_bw * intensidad)
        if pixel_bw > 255:
            pixel_bw = 255
        lista[i] = pixel_bw
        lista[i + 1] = pixel_bw
        lista[i + 2] = pixel_bw
    return lista
