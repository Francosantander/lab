import sys
import argparse
import os


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
    width = header[2:6]
    height = header[7:10]
    header = header[0:2] + "\n" + comentario + header[2:]
    return header, width, height


def argumentos():
    # parser = ArgumentParser(description='TP1')
    # creo la instancia del parser
    parser = argparse.ArgumentParser(description='Trabajo Practico Nº3'
                                                 ' - Server')
    parser.add_argument('-p', '--port', default='5000',
                        help='puerto donde espera nuevas conexiones', type=int)
    parser.add_argument('-s', '--size', default=1026,
                        help='bloque de lectura', type=int)
    parser.add_argument('-d', '--document_root', default='No ingreso nada',
                        help='directorio donde se encuentran los documentos', type=str)
    args = parser.parse_args()
    # hago un manejo de error en caso de que ingrese un document-root vacio
    text = ""
    try:
        if args.document_root == "No ingreso nada":
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
        if int(args.port) < 0:
            raise ValError()
    except ValError:
        print("Error. El puerto a conectar debe ser un valor entero positivo")
        sys.exit()
    try:
        path = args.document_root
        os.chdir(path)
    except FileNotFoundError:
        print("Error. Ingrese un path que exista")
        sys.exit()
    return args
