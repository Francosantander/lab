import os
from funciones import argumentos
import array
from filtros import hilos, procesar


def datos(enviado):
    try:
        encabezado = enviado.decode().splitlines()[0]  # obtengo la primer linea
        archivo = "." + encabezado.split()[1]  # obtengo lo que me solicita el cliente
        archivo = index(archivo)
    except IndexError:
        encabezado = enviado.decode().splitlines()[0]  # obtengo la primer linea
        archivo = "." + encabezado.split()[1]  # obtengo lo que me solicita el cliente
        archivo = index(archivo)
    try:
        extension = archivo.split('.')[2]  # obtengo la extension del archivo
    except IndexError:
        extension = archivo
    try:
        if (archivo.split('.')[2])[3] == "?":
            extension = archivo.split('.')[2]
            query = extension.split('?')[1]
            extension = extension.split('?')[0]
        else:
            query = ""
    except IndexError:
        query = ""
    return encabezado, archivo, extension, query


def index(archivo):
    if archivo == './':
        archivo = './index.html'
    return archivo


def error404(archivo):
    if os.path.isfile(archivo) is False:  # si no esta el archivo
        archivo = './400error.html'
    return archivo


def tamano(size):
    if size % 3 != 0:
        size += (3 - (size % 3))
    return size


def leer_archivo(archivo, size):
    fd = os.open(archivo, os.O_RDONLY)
    body = ""
    lista = []
    while True:
        body = os.read(fd, size)
        lista += [i for i in body]
        if len(body) != size:
            break
    body = array.array('B', lista)
    os.close(fd)
    return body


def curso_normal(encabezado, archivo, extension):
    args = argumentos()
    dic = {"txt": "text/plain", "jpg": "image/jpeg", "ppm": "image/x-portable-pixmap", "html": "text/html", "pdf": "application/pdf"}
    # document-root
    if archivo == './index.html':
        path = '/home/franco/compu2/lab/alumnos/58105-franco-santander/tp3/'
        os.chdir(path)
        extension = archivo.split('.')[2]
    else:
        path = args.document_root
        os.chdir(path)
        # Verifico si se puede abrir el archivo, sino devuelvo un 404
        archivo = error404(archivo)
        extension = archivo.split('.')[2]
    size = tamano(args.size)
    if archivo == './400error.html':
        path = '/home/franco/compu2/lab/alumnos/58105-franco-santander/tp3/'
        os.chdir(path)
        body = leer_archivo(archivo, size)
        header = bytearray("HTTP/1.1 404 Not Found\nContent-Type:" + dic[extension] + "\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
    else:
        body = leer_archivo(archivo, size)
        header = bytearray("HTTP/1.1 200 OK\r\nContent-type:" + dic[extension] + "\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
    return header, body


def curso_ppm(encabezado, archivo, extension):
    args = argumentos()
    dic = {"txt": "text/plain", "jpg": "image/jpeg", "ppm": "image/x-portable-pixmap", "html": "text/html", "pdf": "application/pdf"}
    query_pos = archivo.find('m')
    query = archivo[query_pos+1:]
    if query == "":
        header, body = curso_normal(encabezado, archivo, extension)
    elif query != "":
        # cambio el path
        path = args.document_root
        os.chdir(path)
        # veo que la query no este vacia
        if query == "?":
            archivo = './500error.html'
        else:
            # obtengo la query y la divido en el filtro y la escala
            query.lower()
            archivo = verify_query(query, archivo)
            if archivo == './400error.html' or archivo == './500error.html':
                archivo = archivo
            else:
                try:
                    val_escala = float((query[1:].split('&')[1]).split('=')[1])
                    if val_escala > 0:
                        val_escala = val_escala
                    else:
                        print("El valor de la intensidad no puede ser negativo")
                        archivo = './500error.html'
                except ValueError:
                    archivo = archivo
        # Curso normal + query
        if archivo == './400error.html' or archivo == './500error.html':
            archivo = archivo
        else:
            archivo = archivo.split('?')[0]
        size = args.size
        if archivo == './400error.html':
            path = '/home/franco/compu2/lab/alumnos/58105-franco-santander/tp3/'
            os.chdir(path)
            extension = archivo.split('.')[2]
            body = leer_archivo(archivo, size)
            header = bytearray("HTTP/1.1 404 Not Found\nContent-Type:" + dic[extension] + "\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
        elif archivo == './500error.html':
            path = '/home/franco/compu2/lab/alumnos/58105-franco-santander/tp3/'
            os.chdir(path)
            extension = archivo.split('.')[2]
            body = leer_archivo(archivo, size)
            header = bytearray("HTTP/1.1 500 Internal Server Error\nContent-Type:" + dic[extension] + "\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')
        else:
            filtro = (query.split('&')[0]).split('=')[1]
            sizefile = os.stat(archivo).st_size
            cant_hilos, size = hilos(size, sizefile)
            body = procesar(cant_hilos, size, archivo, filtro, val_escala)
            extension = archivo.split('.')[2]
            header = bytearray("HTTP/1.1 200 OK\r\nContent-type:" + dic[extension] + "\r\nContent-length:"+str(len(body))+"\r\n\r\n", 'utf8')
    return header, body


def verify_query(query, arch):
    if len(query) == 19 or len(query) == 21 or len(query) == 22 or len(query) == 23 or len(query) == 24:
        query = query[1:]
        simbolo = query.find("&")
        has = query[simbolo]
        filtro = query.split('&')[0]
        simbolo2 = filtro.find("=")
        igual = filtro[simbolo2]
        filtro = filtro.split('=')[0]
        escala = query.split('&')[1]
        simbolo3 = escala.find('=')
        igual2 = escala[simbolo3]
        if has == "&" and igual == "=" and igual2 == "=":
            if filtro == "filtro":
                color = (query.split('&')[0]).split('=')[1]
                if color == "rojo" or color == "verde" or color == "azul" or color == "bw":
                    escala = (query.split('&')[1]).split('=')[0]
                    if escala == "escala":
                        escala = (query[1:].split('&')[1]).split('=')[1]
                        if escala != "":
                            archivo = arch
                        else:
                            archivo = './400error.html'
                    else:
                        archivo = './400error.html'
                else:
                    archivo = './400error.html'
            else:
                archivo = './400error.html'
        else:
            archivo = './400error.html'
    else:
        archivo = './500error.html'
    return archivo
