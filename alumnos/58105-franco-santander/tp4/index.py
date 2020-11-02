from os import scandir
import os


def generar_index(abspath):
    html = "<!DOCTYPE html>\n<html>\n<head><meta charset=\"UTF-8\">\n<title>Index</title>\n</head>\n<body>\n"
    html += "<h2>Bienvenido a comp2</h2>\n"
    path = os.getcwd()
    archivos = [obj.name for obj in scandir(path) if obj.is_file()]
    for archivo in archivos:
        if ".py" not in archivo:
            html += "<li><a href=\"{}\">{}</a></li>\n".format(archivo, archivo)
    html += "</body>\n</html>"
    file = open(f"{abspath}/html/index.html", "w")
    file.write(html)
    file.close()


def generateHeader(path, abspath):
    dic = {"jpg": "image/jpeg", "pdf": "application/pdf", "html": "text/html", "ppm": "image/x-portable-pixmap"}
    if os.path.exists(path):
        try:
            extension = path.split(".")[1]
            extension = dic[extension]
            codeR = "HTTP/1.1 200 OK"
        except KeyError:
            codeR = "HTTP/1.1 500 Internal Server Error"
            path = f"{abspath}/html/500error.html"
    else:
        path = f"{abspath}/html/400error.html"
        codeR = "HTTP/1.1 404 Not Found"
    extension = path.split(".")[1]
    size = os.stat(path).st_size
    header = "{}\r\nContent-type: {}\r\nContent-lenght: {}\r\n\r\n".format(codeR, dic[extension], size)
    header = bytearray(header, "utf8")
    return path, header
