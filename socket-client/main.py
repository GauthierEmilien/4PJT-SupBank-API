from Client import Client
import socketio
from aiohttp import web, web_request
from threading import Lock
from Cryptodome.PublicKey import RSA
from Transaction import Transaction
from Blockchain import Blockchain

server = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
server.attach(app)
node_ip = ''

lock = Lock()

eric_key = RSA.generate(1024)
alex_key = RSA.generate(1024)
my_key = RSA.generate(1024)

xatome_money = Blockchain()


# On button click
async def index(request):
    transaction = Transaction(eric_key.publickey().export_key('DER'), alex_key.publickey().export_key('DER'), 20)
    transaction.sign(eric_key)

    lock.acquire()
    for node in Client.nodes_info:
        if node.get('host') != node_ip:
            client = Client(node.get('host'), is_node=True)
            client.start()
            client.join()
            client.send_transaction(transaction)
    lock.release()
    return web.Response(text="Message sent to all connected nodes")


@server.on('connect')
async def connect(sid, environ: dict):
    req: web_request.Request = environ.get('aiohttp.request')
    ip = req.transport.get_extra_info('peername')[0]
    print('\nREMOTE CONNECTED => {} ({})'.format(ip, sid))

    lock.acquire()
    Client.connected_nodes.append({'sid': sid, 'host': ip})
    print('CONNECTED NODES => {}'.format(Client.connected_nodes))
    lock.release()


@server.on('disconnect')
async def disconnect(sid):
    print('\nREMOTE DISCONNECTED => {}'.format(sid))
    lock.acquire()
    Client.connected_nodes[:] = [n for n in Client.connected_nodes if n.get('sid') != sid]
    print('CONNECTED NODES => {}'.format(Client.connected_nodes))
    lock.release()


@server.on('transaction')
async def on_test(sid, transaction_data):
    transaction = Transaction.from_dict(transaction_data)
    print('TRANSACTION FROM {} => {}'.format(sid, transaction.__dict__()))
    xatome_money.add_transaction(transaction)
    print('{} pending transaction(s)'.format(len(xatome_money.get_pending_transaction())))
    if len(xatome_money.get_pending_transaction()) >= 5:
        xatome_money.mine_pending_trans(my_key.publickey().export_key('DER'))


app.router.add_get('/', index)

if __name__ == '__main__':
    ip = str(input('Which ip : '))
    client_server_ip = Client(ip, 'server_ip_connection')

    try:
        client_server_ip.start()
        client_server_ip.join()
        node_ip = client_server_ip.get_node_ip()
        web.run_app(app, host=node_ip, port=8000)
    except Exception as e:
        print('error =>', e)
