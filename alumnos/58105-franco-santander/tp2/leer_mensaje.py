import os


def leer_mensaje(menssage, size):
    mensaje = os.open(menssage, os.O_RDONLY)  # Abro mensaje a leer
    mensaje_leido = os.read(mensaje, size)  # Leo mensaje
    lista_mensaje = []
    for i in mensaje_leido:
        lista_mensaje.append("{0:b}".format(i))
    contador = 0
    for caracteres in lista_mensaje:
        for i in range(8-(len(caracteres))):
            caracter = "0" + caracteres
        lista_mensaje[contador] = caracter
        contador += 1
    mensaje_binario = ""
    for i in lista_mensaje:
        mensaje_binario += i
    longuitud = len(mensaje_binario)
    return mensaje_binario, longuitud
