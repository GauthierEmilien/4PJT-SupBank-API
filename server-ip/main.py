import socketio
from aiohttp import web, web_request, ClientSession
from typing import List
import netifaces as ni
from PyInquirer import prompt
from random import randrange

from database import DB

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
routes = web.RouteTableDef()
sio.attach(app)

nodes: List[dict] = []
database = DB('xatomeDB')

@routes.post('/login')
async def login(request: web_request.Request):
    print(request)
    return web.json_response({'coucou': 'bonjour'})

@routes.post('/register')
async def register(request: web_request.Request):
    user: dict = await request.json()
    existing_user = database.get_one('users', {'email': user.get('email')})
    if existing_user:
        return web.json_response({'error': 'User already exists in database'})
    else:
        res = user.copy()
        database.insert('users', user)
        return web.json_response(res)

@routes.get('/blockchain')
async def get_blockchain(_):
    if len(nodes) > 0:
        index = 0 if len(nodes) == 1 else randrange(len(nodes))
        async with ClientSession() as session:
            async with session.get('http://' + nodes[index].get('host') + ':8000/blockchain') as resp:
                print('resp type', type(resp))
                chain = await resp.json()
                print('chain', chain)

        return web.json_response(chain)
    return web.Response(text='no nodes connected')


app.add_routes(routes)

@sio.on('connect')
async def connect(sid, environ: dict):
    print('connect ', sid)
    req: web_request.Request = environ.get('aiohttp.request')
    ip = req.transport.get_extra_info('peername')[0]
    nodes.append({'sid': sid, 'host': ip})
    print(nodes)
    await sio.emit('ip', ip, room=sid)
    await sio.emit('nodes', nodes)


@sio.on('disconnect')
async def disconnect(sid):
    nodes[:] = [n for n in nodes if n.get('sid') != sid]
    print(nodes)
    await sio.emit('nodes', nodes)


def get_ip_addresses() -> List[str]:
    ip_addresses: List[str] = []
    for int in ni.interfaces():
        net: List[dict] = ni.ifaddresses(int).get(ni.AF_INET)
        if net and net[0].get('addr') != '127.0.0.1':
            ip_addresses.append(net[0].get('addr'))
    return ip_addresses


def choose_ip_address(ip_addresses: List[str]) -> str:
    for index, addr in enumerate(ip_addresses):
        print('{}) {}'.format(index + 1, addr))

    num = -1
    while num < 1 or num > len(ip_addresses):
        num = int(input('Choose your wifi card ip: '))
    return ip_addresses[num - 1]


if __name__ == '__main__':
    ip_addresses = get_ip_addresses()
    ip_server = ''

    try:
        questions: List[dict] = [
            {
                'type': 'list',
                'name': 'ip',
                'message': 'Choose your wifi card ip',
                'choices': ip_addresses
            }
        ]

        answers = prompt(questions)
        ip_server = answers.get('ip')
    except:
        ip_server = choose_ip_address(ip_addresses)

    print(ip_server)

    if ip_server:
        print('To deploy server (Ubuntu 18):\n- sudo ufw enable && sudo ufw allow 8000\n')
        print('Server ip to connect :', ip_server)
        web.run_app(app, host=ip_server, port=8000)
    else:
        print('No ip provided')
