import socketio
import socket
import atexit

sio = socketio.Client()


def exit_handler():
    sio.disconnect()


atexit.register(exit_handler)


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


if __name__ == '__main__':
    try:
        sio.connect('http://localhost:5000')

    except Exception:
        print('Unable to connect to server')
