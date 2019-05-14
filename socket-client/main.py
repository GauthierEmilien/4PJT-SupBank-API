import socketio
import netifaces as ni

### ASYNC VERSION ###
# sio = socketio.AsyncClient()
# loop = asyncio.get_event_loop()
#
#
# @sio.on('connect')
# async def on_connect():
#     print('I\'m connected!')
#     hostname = socket.gethostname()
#     ip = socket.gethostbyname(hostname)
#     print(hostname, ip)
#     await sio.emit('ip-address', {'hostname': hostname, 'ip': ip})
#
#
# @sio.on('nodes')
# def on_nodes(data):
#     print(data)
#
#
# @sio.on('disconnect')
# def on_disconnect():
#     print('I\'m disconnected!')
#
#
# async def start_client():
#     await sio.connect('http://localhost:5000')
#     await sio.wait()
#
#
# if __name__ == '__main__':
#     try:
#         loop.run_until_complete(start_client())
#     except Exception:
#         print('Unable to connect to server')

sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print('I\'m connected!')
    ip = ni.ifaddresses(ni.interfaces()[-1])[ni.AF_INET][0]['addr']
    sio.emit('ip-address', {'ip': ip})


@sio.on('nodes')
def on_nodes(data):
    print(data)


@sio.on('disconnect')
def on_disconnect():
    print('I\'m disconnected!')


def start_client(ip: str):
    sio.connect('http://{}:8000'.format(ip))


if __name__ == '__main__':
    ip = str(input('Which ip : '))
    try:
        start_client(ip)
    except Exception:
        print('Unable to connect to server')
