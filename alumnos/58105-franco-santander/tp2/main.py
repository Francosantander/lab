import os
import threading
from leer_mensaje import leer_mensaje
from funciones import eliminar_comentario, header, calcular_posicion
from funciones import argumentos
import array
from time import time


class OverflowError(Exception):
    def __init__(self, message):
        print(message)


global lista
lista = []
global imagen_leida
imagen_leida = ""
lc = threading.Lock()


# funcion para obtener argumentos
def main():
    tiempo_inicio = time()
    # Creo los argumentos
    args = argumentos()
    size = int(args.size)
    # Verifico que el pixel este completo
    if size % 3 != 0:
        size += (3 - (size % 3))
    # Genero el path absoluto
    # path = os.path.abspath(os.getcwd())
    # abro la imagen
    archivo = os.open(args.file, os.O_RDONLY)
    # abro la imagen y lo guardo en imagen
    imagen = os.read(archivo, size)
    # abro el mensaje y obtengo una str con el mensaje en bit
    # mensaje = open(path + "/" + args.message, "rb")
    message, long_men = leer_mensaje(args.message, size)
    # paso a int el interleave y el offset
    interleave = int(args.interleave)
    offset = int(args.offset)
    # calculo la posicion donde comienza el cuerpo de la imagen
    posicion = calcular_posicion(imagen)
    # Creo el comentario, elimino si hay algun comentario en la imagen y
    # creo la cabecera del nuevo archivo
    comentario = "#UMCOMPU2 {} {} {}".format(offset, interleave, long_men)
    texto1 = eliminar_comentario(imagen)
    cabecera, width, height = header(texto1, comentario)
    if long_men * interleave + offset > int(width) * int(height):
        raise OverflowError("No hay bytes suficientes en la imagen para"
                            "insertar el mensage con el interleave y"
                            " el offset ingresados")
    # Me paro donde inicia el curpo en la imagen
    os.lseek(archivo, posicion, 0)
    # Creo el output y le paso el header
    output = open(args.output, "wb", os.O_CREAT)
    output.write(bytearray(cabecera, 'ascii'))
    # declaro global las variables donde se almacena lo leido de la imagen y
    # la lista donde lo guardo
    global imagen_leida
    global lista
    while True:
        # Creo hilos
        hilo_rojo = threading.Thread(target=encriptar_rojo, args=(interleave,
                                     offset, message))
        hilo_verde = threading.Thread(target=encriptar_verde, args=(interleave,
                                      offset, message))
        hilo_azul = threading.Thread(target=encripar_azul, args=(interleave,
                                     offset, message))
        # Pongo un lock para leer la imagen
        lc.acquire
        imagen_leida = os.read(archivo, size)
        lista = [i for i in imagen_leida]
        lc.release
        hilo_rojo.start()
        hilo_verde.start()
        hilo_azul.start()
        # print("entro")
        hilo_rojo.join()
        hilo_verde.join()
        hilo_azul.join()
        # print("salio")
        lc.acquire
        imagen_nueva = array.array('B', lista)
        imagen_nueva.tofile(output)
        lc.release
        if len(imagen_leida) != size:
            break
    output.close()
    print("Se genero correctamente, el proceso tardo: ")
    print(time() - tiempo_inicio, " segundos")


def encriptar_rojo(interleave, offset, mensaje):
    # Indices del mensaje para cada color
    c_r = 0  # 0, 3, 6, 9
    global lista
    # Indices para la lista
    # Rojo
    ini_r = 0 + ((3*offset))
    fin_r = len(lista)
    for j in range(ini_r, fin_r, (interleave*9)):
        if c_r < len(mensaje):
            lc.acquire()
            if lista[j] % 2 == 0:
                if mensaje[c_r] == "0":
                    lista[j] = lista[j]
                else:
                    lista[j] += 1
            else:
                if mensaje[c_r] == "1":
                    lista[j] = lista[j]
                else:
                    lista[j] -= 1
            lc.release()
            c_r += 3


def encriptar_verde(interleave, offset, mensaje):
    c_v = 1  # 1, 4, 7, 10
    global lista
    # verde
    ini_v = 1 + (3*(offset)) + (3*(interleave))
    fin_v = len(lista)
    for j in range(ini_v, fin_v, (interleave*9)):
        if c_v < len(mensaje):
            lc.acquire()
            if lista[j] % 2 == 0:
                if mensaje[c_v] == "0":
                    lista[j] = lista[j]
                else:
                    lista[j] += 1
            else:
                if mensaje[c_v] == "1":
                    lista[j] = lista[j]
                else:
                    lista[j] -= 1
            lc.release()
            c_v += 3


def encripar_azul(interleave, offset, mensaje):
    c_b = 2  # 2, 5, 8, 11
    global lista
    # azul
    ini_b = 2 + (3*(offset) + ((interleave)*6))
    fin_b = len(lista)
    for j in range(ini_b, fin_b, (interleave*9)):
        if c_b < len(mensaje):
            lc.acquire()
            if lista[j] % 2 == 0:
                if mensaje[c_b] == "0":
                    lista[j] = lista[j]
                else:
                    lista[j] += 1
            else:
                if mensaje[c_b] == "1":
                    lista[j] = lista[j]
                else:
                    lista[j] -= 1
            lc.release()
            c_b += 3


if __name__ == "__main__":
    main()
