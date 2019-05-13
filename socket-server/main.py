import socketio
from aiohttp import web
from typing import List

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

nodes: List[dict] = []


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)


@sio.on('ip-address')
async def on_ip_address(sid, data: dict):
    nodes.append({'sid': sid, 'host': data})
    print(nodes)
    await sio.emit('nodes', nodes)


@sio.on('disconnect')
async def disconnect(sid):
    nodes[:] = [n for n in nodes if n.get('sid') != sid]
    print(nodes)
    await sio.emit('nodes', nodes)

async def index(request):
    return web.Response(text='bonjour')

app.router.add_get('/', index)


if __name__ == '__main__':
    web.run_app(app, host='localhost', port=5000)
