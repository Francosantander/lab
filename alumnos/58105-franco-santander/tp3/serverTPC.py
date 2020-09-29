#!/usr/bin/python3
import socketserver
from funciones import argumentos
from ErroresYDemas import curso_normal, datos, curso_ppm
# import threading


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024)
        encabezado, archivo, extension, query = datos(self.data)
        if extension == "ppm" or query != "":
            header, body = curso_ppm(encabezado, archivo, extension)
        # ver si modifico para que sea elif en ves de else, error500
        else:
            header, body = curso_normal(encabezado, archivo, extension)
        self.request.sendall(header)
        self.request.sendall(body)


args = argumentos()
socketserver.ThreadingTCPServer.allow_reuse_address = True
server = socketserver.ThreadingTCPServer(("0.0.0.0", args.port), Handler)
server.serve_forever()
