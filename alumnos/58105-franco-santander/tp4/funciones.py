import sys
import argparse
import os


class ArchivoError(Exception):
    pass


class ValError(Exception):
    pass


def argumentos():
    # parser = ArgumentParser(description='TP1')
    # creo la instancia del parser
    parser = argparse.ArgumentParser(description='Trabajo Practico Nº4'
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
        text += "Error. Ingrese un archivo que se encuentre en el"
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
