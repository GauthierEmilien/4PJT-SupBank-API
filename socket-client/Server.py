import socketio
from aiohttp import web, web_request
import Client
from Transaction import Transaction
from threading import Lock
from random import randrange
import global_var

lock = Lock()


class Server:

    def __init__(self):
        self.__host = ''
        self.__port = 0
        self.__server = socketio.AsyncServer(async_mode='aiohttp')
        self.__app = web.Application()
        self.__server.attach(self.__app)
        self.__setup_callbacks()

    def __setup_callbacks(self):
        self.__server.on('connect', self.__on_connect)
        self.__server.on('disconnect', self.__on_disconnect)
        self.__server.on('transaction', self.__on_transaction)
        self.__server.on('blockchain', self.__on_blockchain)
        self.__server.on('block', self.__on_block)
        self.__app.router.add_get('/transaction', self.__make_transaction)
        self.__app.router.add_get('/blockchain', self.__update_blockchain)

    async def __on_connect(self, sid, environ: dict):
        req: web_request.Request = environ.get('aiohttp.request')
        ip = req.transport.get_extra_info('peername')[0]
        print('\nREMOTE CONNECTED => {} ({})'.format(ip, sid))
        lock.acquire()
        Client.Client.connected_nodes.append({'sid': sid, 'host': ip})
        print('CONNECTED NODES => {}'.format(Client.Client.connected_nodes))
        lock.release()

    async def __on_disconnect(self, sid):
        print('\nREMOTE DISCONNECTED => {}'.format(sid))
        lock.acquire()
        Client.Client.connected_nodes[:] = [n for n in Client.Client.connected_nodes if n.get('sid') != sid]
        print('CONNECTED NODES => {}'.format(Client.Client.connected_nodes))
        lock.release()

    async def __on_transaction(self, sid, transaction_data: dict):
        transaction = Transaction.from_dict(transaction_data)
        print('TRANSACTION FROM {} => {}'.format(sid, transaction.__dict__()))
        global_var.xatome_money.add_transaction(transaction)
        print('{} pending transaction(s)'.format(len(global_var.xatome_money.get_pending_transaction())))
        if len(global_var.xatome_money.get_pending_transaction()) >= 5:
            global_var.xatome_money.start(global_var.my_key.publickey().export_key('DER'))

    async def __on_blockchain(self, sid):
        print('SEND BLOCKCHAIN TO => {}'.format(sid))
        await self.__server.emit('blockchain', [b.__dict__() for b in global_var.xatome_money.get_blocks()], room=sid)

    async def __on_block(self, sid, block_data: dict):
        print('GET BLOCK FROM => {}'.format(sid))

        from Block import Block
        from global_var import xatome_money
        from Blockchain import Blockchain
        block = Block.from_dict(block_data)
        if xatome_money.is_chain_valid(block):
            Blockchain.add_block(block)
            await self.__server.emit('block', 'true', room=sid)
        else:
            await self.__server.emit('block', 'false', room=sid)

    async def __make_transaction(self, request):
        transaction = Transaction(global_var.eric_key.publickey().export_key('DER'),
                                  global_var.alex_key.publickey().export_key('DER'), 20)
        transaction.sign(global_var.eric_key)

        self.__send_to_every_nodes('transaction', transaction.__dict__())
        return web.Response(text="Message sent to all connected nodes")

    async def __update_blockchain(self, request):
        print('update blockchain')
        lock.acquire()
        nodes_info = [c for c in Client.Client.nodes_info if c.get('host') != self.__host]
        lock.release()
        index = 0 if len(nodes_info) < 1 else randrange(len(nodes_info))
        client = Client.Client(nodes_info[index].get('host'))
        client.start()
        client.join()
        client.send_message('blockchain', disconnect=False)
        print('waiting for blockchain update')
        client.wait()
        return web.Response(text="waiting for updated blockchain")

    def start(self, host: str, port: int):
        self.__host = host
        self.__port = port
        try:
            web.run_app(self.__app, host=host, port=port)
        except Exception as e:
            print('error from class Server =>', e)

    def __send_to_every_nodes(self, topic: str, data, disconnect=True):
        lock.acquire()
        for node in Client.Client.nodes_info:
            if node.get('host') != self.__host:
                client = Client.Client(node.get('host'))
                client.start()
                client.join()
                client.send_message(topic, data, disconnect)
        lock.release()

    def send_block(self, block: dict):
        self.__send_to_every_nodes('block', block, False)
