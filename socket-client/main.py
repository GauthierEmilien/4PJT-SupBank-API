import asyncio
import socketio
import socket
import atexit

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
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(hostname, ip)
    sio.emit('ip-address', {'hostname': hostname, 'ip': ip})


@sio.on('nodes')
def on_nodes(data):
    print(data)


@sio.on('disconnect')
def on_disconnect():
    print('I\'m disconnected!')


def start_client():
    sio.connect('http://localhost:5000')


if __name__ == '__main__':
    try:
        start_client()
    except Exception:
        print('Unable to connect to server')
