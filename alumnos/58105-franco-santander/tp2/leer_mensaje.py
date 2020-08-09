import os


def leer_mensaje(message, size):
    mensaje = os.open(message, os.O_RDONLY)  # Abro mensaje a leer
    mensaje_leido = os.read(mensaje, size)  # Leo mensaje
    # print(mensaje_leido)

    lista_mensaje = []
    for i in mensaje_leido:
        lista_mensaje.append("{0:b}".format(i))

    contador = 0

    for caracteres in lista_mensaje:
        for i in range(8-(len(caracteres))):
            caracteres = "0" + caracteres

        lista_mensaje[contador] = caracteres
        contador += 1

    mensaje_binario = ""  # Queda mensaje en ceros y unos como un solo texto

    for caracteres in lista_mensaje:
        mensaje_binario = mensaje_binario + caracteres
    longitud = len(mensaje_binario)
    return mensaje_binario, longitud
