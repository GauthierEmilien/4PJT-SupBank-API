from Client import Client
import socketio
from aiohttp import web


server = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
server.attach(app)



if __name__ == '__main__':
    ip = str(input('Which ip : '))
    client_server_ip = Client(ip, 'server_ip_connection')

    client_server_ip.start()

    client_server_ip.join()
    web.run_app(app, host=client_server_ip.get_node_ip(), port=8001)
