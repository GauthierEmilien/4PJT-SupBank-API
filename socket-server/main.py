import socketio
from aiohttp import web
from typing import List
import netifaces as ni

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
    ip = ni.ifaddresses(ni.interfaces()[-1])[ni.AF_INET][0]['addr']
    print('To deploy server (Ubuntu 18):\n- sudo ufw enable && sudo ufw allow 8000\n')
    print('Server ip to connect :', ip)
    web.run_app(app, host=ip, port=8000)
