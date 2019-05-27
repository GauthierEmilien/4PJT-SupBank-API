from Client import Client
import socketio
from aiohttp import web, web_request
from threading import Lock
from Cryptodome.PublicKey import RSA
from Transaction import Transaction
from Blockchain import Blockchain
from random import randrange

server = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
server.attach(app)
node_ip = ''

lock = Lock()

eric_key = RSA.generate(1024)
alex_key = RSA.generate(1024)
my_key = RSA.generate(1024)

xatome_money = Blockchain()
xatome_money.get_update()


# On button click
async def index(request):
    transaction = Transaction(eric_key.publickey().export_key('DER'), alex_key.publickey().export_key('DER'), 20)
    transaction.sign(eric_key)

    lock.acquire()
    for node in Client.nodes_info:
        if node.get('host') != node_ip:
            client = Client(node.get('host'))
            client.start()
            client.join()
            client.send_transaction(transaction)
    lock.release()
    return web.Response(text="Message sent to all connected nodes")


async def update_blockchain(request):
    print('update blockchain')
    lock.acquire()
    nodes_info = [c for c in Client.nodes_info if c.get('host') != node_ip]
    lock.release()
    index = 0 if len(nodes_info) < 1 else randrange(len(nodes_info))
    client = Client(nodes_info[index].get('host'))
    client.start()
    client.join()
    client.ask_for_blockchain()
    print('waiting for blockchain update')
    xatome_money.get_update()
    return web.Response(text="waiting for updated blockchain")


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


@server.on('blockchain')
async def on_blockchain(sid):
    print('SEND BLOCKCHAIN TO => {}'.format(sid))
    await server.emit('blockchain', [b.__dict__() for b in xatome_money.get_blocks()], room=sid)


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
