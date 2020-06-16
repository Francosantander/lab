import os
import threading
from leer_mensaje import leer_mensaje
import concurrent.futures
from funciones import eliminar_comentario, header, calcular_posicion
from funciones import argumentos
import array
from time import time


global lista
lista = []
global imagen_leida
imagen_leida = ""
b = threading.Barrier(4)
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
    path = os.path.abspath(os.getcwd())
    # abro la imagen
    archivo = os.open(args.file, os.O_RDONLY)
    # Calculo el tamaño de la imagen
    tam_ima = os.path.getsize(path + "/" + args.file)
    # abro la imagen y lo guardo en imagen
    imagen = os.read(archivo, size)
    # abro el mensaje y obtengo una str con el mensaje en bit
    mensaje = open(path + "/" + args.message, "rb")
    mensaje, long_men = leer_mensaje(args.message, size)
    # paso a int el interleave y el offset
    interleave = int(args.interleave)
    offset = int(args.offset)
    # calculo la posicion donde comienza el cuerpo de la imagen
    posicion = calcular_posicion(imagen)
    # Creo el comentario, elimino si hay algun comentario en la imagen y
    # creo la cabecera del nuevo archivo
    comentario = "#UMCOMPU2 {} {} {}".format(offset, interleave, long_men)
    texto1 = eliminar_comentario(imagen)
    cabecera = header(texto1, comentario)
    # Me paro donde inicia el curpo en la imagen
    os.lseek(archivo, posicion, 0)
    # Creo el output y le paso el header
    output = open(args.output, "wb", os.O_CREAT)
    output.write(bytearray(cabecera, 'ascii'))
    # Creo hilos
    hilos = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    for i in range(3):
        # i = indice
        hilos.submit(encriptar, interleave, offset, mensaje, i, size)
    # declaro global las variables donde se almacena lo leido de la imagen y
    # la lista donde lo guardo
    global imagen_leida
    global lista
    while True:
        # Pongo un lock para leer la imagen
        lc.acquire
        imagen_leida = os.read(archivo, size)
        lista = [i for i in imagen_leida]
        lc.release
        print("entro")
        b.wait()
        print("salio")
        imagen_nueva = array.array('B', lista)
        imagen_nueva.tofile(output)
        if len(imagen_leida) != size:
            break
    output.close()
    print("Se genero correctamente, el proceso tardo: ")
    print(time() - tiempo_inicio, " segundos")


def encriptar(interleave, offset, mensaje, indice, size):
    global imagen_leida
    global lista
    # Indices del mensaje para cada color
    c_r = 0  # 0, 3, 6, 9
    c_v = 1  # 1, 4, 7, 10
    c_b = 2  # 2, 5, 8, 11
    # Indices para la lista
    # Rojo
    ini_r = 0 + (3*offset)
    fin_r = ini_r + len(mensaje) * (interleave * 3)
    # verde
    ini_v = 4 + (3*(int(offset)) + ((int(interleave)-1)*3))
    if interleave == 1:
        ini_v = 4 + (3*(int(offset)))
    fin_v = ini_v + len(mensaje)*(int(interleave)*3)
    # azul
    ini_b = 8 + (3*(offset)) + interleave + (((int(interleave)-2)*3))
    if interleave == 1:
        ini_b = 8 + (3*(int(offset)))
    fin_b = ini_b + len(mensaje) * (int(interleave)*3)
    while True:
        if indice == 0:  # rojo
            # offset == pixel en el cual comienza ,
            #  interleave == Saltos de pixel
            # offset 0 == 1° pixel, interleave 1 == proximo pixel
            # offset 0 e interleave 1 el rojo se mueve cada 9 lugares
            # offset se multiplica por 3 y el interleva tambien
            if c_r < len(mensaje):
                for j in range(ini_r, fin_r, (interleave*9)):
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
                    c_r += 3
                    lc.release()
        elif indice == 1:
            if c_v < len(mensaje):
                for j in range(ini_v, fin_v, (interleave*9)):
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
                    c_v += 3
                    lc.release()
        else:
            if c_b < len(mensaje):
                for j in range(ini_b, fin_b, (interleave*9)):
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
                    c_b += 3
                    lc.release()
        b.wait()
        if len(imagen_leida) < size:
            break


if __name__ == "__main__":
    main()
