import sys
import argparse


class ArchivoError(Exception):
    pass


class ValError(Exception):
    pass


def eliminar_comentario(texto):
    # Le saco el comentario a la imagen
    text = texto
    for i in range(text.count(b"\n#")):
        inicio = text.find(b"\n# ")
        fin = text.find(b"\n", inicio + 1)
        text = text.replace(text[inicio:fin], b"")
    return text


def header(text, comentario):
    # Le saco el encabezado a la imagen
    header = text[:15].decode()
    # Le agrego el comentario
    header = header[0:2] + "\n" + comentario + header[2:]
    return header


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


def argumentos():
    # parser = ArgumentParser(description='TP1')
    # creo la instancia del parser
    parser = argparse.ArgumentParser(description='Trabajo Practico Nº2'
                                                 ' - Procesa ppm')
    parser.add_argument('-f', '--file', default='',
                        help='archivo portador', type=str)
    parser.add_argument('-s', '--size', default=1026,
                        help='bloque de lectura', type=int)
    parser.add_argument('-m', '--message', default='',
                        help='mensaje esteganográfico', type=str)
    parser.add_argument('-e', '--offset', default=1,
                        help='offset en pixels del inicio del raster',
                        type=int)
    parser.add_argument('-i', '--interleave', default=1,
                        help='interleave de modificacion en pixel',
                        type=int)
    parser.add_argument('-o', '--output', default='encriptado.ppm',
                        help='entrego mesaje', type=str)
    args = parser.parse_args()
    # hago un manejo de error en caso de que ingrese un archivo vacio
    text = ""
    try:
        if args.file == "No ingreso nada":
            raise ArchivoError()
    except ArchivoError:
        text += "Error. Ingrese un archivo ppm que se encuentre en el"
        text += " mismo directorio"
        print(text)
        sys.exit()
    try:
        if int(args.size) < 0:
            raise ValError()
    except ValError:
        print("Error. El tamaño del bloque no puede ser negativo")
        sys.exit()
    try:
        archivo = open(args.file, "rb")
        archivo.close()
    except FileNotFoundError:
        print("Error. El archivo no se encuentra en el directorio")
        sys.exit()
    return args
