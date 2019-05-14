import socketio

sio = socketio.Client()


@sio.on('connect')
def on_connect():
    print('I\'m connected!')


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
