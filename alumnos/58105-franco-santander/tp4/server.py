import asyncio
import socket
from funciones import argumentos
import datetime as dt
import os
from index import generar_index, generateHeader


global abspath


# Manejador del cliente
async def handler(reader, writer):
    addr = writer.get_extra_info('peername')
    asyncio.create_task(generar_logs(addr[0], addr[1]))
    leido = (await reader.read(args.size)).decode()
    if "GET" in leido:
        query = leido.split(" ")[1]
        path = os.getcwd()
        if query == "/":
            path = f"{abspath}/html/index.html"
        else:
            path = f"{path}{query}"
        path, header = generateHeader(path, abspath)
        writer.write(header)
        fdr = os.open(path, os.O_RDONLY)
        while True:
            body = os.read(fdr, args.size)
            writer.write(body)
            if(len(body) != args.size):
                break
        os.close(fdr)
        await writer.drain()
        writer.close()
        await writer.wait_closed()


# Genero el registristro de los clientes
async def generar_logs(ip, port):
    time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registro = "| Cliente: {} | Puerto: {} | Fecha: {} |\n".format(ip, port, time)
    with open(f"{abspath}/log.txt", "a") as file:
        file.write(registro)
    file.close()


# Genero el server y lo inicio
async def server(host, port):
    server = await asyncio.start_server(handler, host, port, family=socket.AF_UNSPEC)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    abspath = os.getcwd()
    args = argumentos()
    generar_index(abspath)
    asyncio.run(server(["127.0.0.1", "::1"], args.port))
