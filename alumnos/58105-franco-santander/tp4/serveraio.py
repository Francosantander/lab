from aiohttp import web
import os
from funciones import argumentos
from index import generar_index
import datetime as dt
import asyncio
routes = web.RouteTableDef()

global abspath


@routes.get('/')
async def hello(request):
    addr = request.transport.get_extra_info('peername')
    asyncio.create_task(generar_logs(addr[0], addr[1]))
    return web.FileResponse(f"/{abspath}/html/index.html")


async def generar_logs(ip, port):
    time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registro = "| Cliente: {} | Puerto: {} | Fecha: {} |\n".format(ip, port, time)
    with open(f"{abspath}/logaio.txt", "a") as file:
        file.write(registro)
    file.close()


abspath = os.getcwd()
args = argumentos()
path = os.getcwd()
generar_index(abspath)
app = web.Application()
app.add_routes(routes)
app.router.add_static("/", "./")
web.run_app(app, host=["127.0.0.1", "::1"], port=args.port)
