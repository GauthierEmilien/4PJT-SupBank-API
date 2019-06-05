from datetime import datetime
from random import randrange
from threading import Lock

import flask
import socketio
from Cryptodome.PublicKey import RSA

from blockchain.Block import Block
from blockchain.Blockchain import Blockchain
from blockchain.Mining import Mining
from blockchain.Transaction import Transaction
from server.Client import Client

lock = Lock()


class Server:

    def __init__(self, parent, host: str, port: int):
        self.__host = host
        self.__port = port
        self.__server = socketio.Server(async_mode='threading')
        self.__app = flask.Flask(__name__)
        self.__app.wsgi_app = socketio.WSGIApp(self.__server, self.__app.wsgi_app)
        self.__setup_callbacks()
        self.__mining_thread = None
        self.__blockchain = Blockchain()
        self.__update_blockchain()
        self.__mining = False
        self.parent = parent

    def __setup_callbacks(self):
        self.__server.on('connect', self.__on_connect)
        self.__server.on('disconnect', self.__on_disconnect)
        self.__server.on('transaction', self.__on_transaction)
        self.__server.on('blockchain', self.__on_blockchain)
        self.__server.on('block', self.__on_block)
        self.__server.on('block_accepted', self.__on_block_accepted)
        self.__app.route('/blockchain', methods=['GET'])(self.__return_blockchain)
        # self.__app.router.add_get('/transaction', self.__make_transaction)

    def __on_connect(self, sid, environ: dict):
        ip = environ.get('REMOTE_ADDR')
        print('\nREMOTE CONNECTED => {} ({})'.format(ip, sid))
        lock.acquire()
        Client.connected_nodes.append({'sid': sid, 'host': ip})
        print('CONNECTED NODES => {}'.format(Client.connected_nodes))
        lock.release()

    def __on_disconnect(self, sid):
        print('\nREMOTE DISCONNECTED => {}'.format(sid))
        lock.acquire()
        Client.connected_nodes[:] = [n for n in Client.connected_nodes if n.get('sid') != sid]
        print('CONNECTED NODES => {}'.format(Client.connected_nodes))
        lock.release()

    def __on_transaction(self, sid, transaction_data: dict):
        transaction = Transaction.from_dict(transaction_data)
        print('TRANSACTION FROM {} => {}'.format(sid, transaction.__dict__()))
        self.__blockchain.add_transaction(transaction)
        print('{} pending transaction(s)'.format(len(self.__blockchain.get_pending_transaction())))
        if self.__mining and len(self.__blockchain.get_pending_transaction()) >= 5:
            if self.__mining_thread is None or (self.__mining_thread and not self.__mining_thread.is_alive()):
                private_key = self.parent.tab_wallet.get_key_object()
                self.__mining_thread = Mining(self.__blockchain, private_key.publickey().export_key('DER'), self.__host,
                                              self.parent)
                self.parent.update()

    def __on_blockchain(self, sid):
        print('SEND BLOCKCHAIN TO => {}'.format(sid))
        self.__server.emit('blockchain', [b.__dict__() for b in self.__blockchain.get_blocks()], room=sid)

    def __on_block(self, sid, block_data: dict):
        print('GET BLOCK FROM => {}'.format(sid))
        if self.__mining_thread and self.__mining_thread.is_alive():
            self.__mining_thread.stop()
            self.__mining_thread.join()
            print('mining thread stopped')

        block = Block.from_dict(block_data)
        if self.__blockchain.is_chain_valid(block):
            self.__server.emit('block', 'true', room=sid)
        else:
            self.__server.emit('block', 'false', room=sid)

    def __on_block_accepted(self, _, block):
        print('GET ACCCEPTED BLOCK => {}'.format(block))
        if block != 'false':
            self.__blockchain.add_block(block)
            self.__blockchain.clear_pending_transaction(block.get('transactions'))
            self.parent.update()
        # else:
        #     print('restart mining')
        #     from Mining import Mining
        #     self.__mining_thread = Mining(global_var.xatome_money, self.__mining_thread.get_reward_address())
        #     self.__mining_thread.start()

    def __return_blockchain(self):
        return flask.jsonify(self.__blockchain.__dict__())

    def make_transaction(self, key_from: RSA.RsaKey, key_to: str, amount: int):
        transaction = Transaction(str(datetime.now()), key_from.publickey().export_key('DER'),
                                  RSA.import_key(key_to).export_key('DER'), amount)
        transaction.sign(key_from)

        Client.send_to_every_nodes(self.__host, 'transaction', transaction.__dict__())
        self.__on_transaction('local', transaction.__dict__())
        self.parent.update()

    def __update_blockchain(self):
        print('update blockchain', Client.nodes_info)
        lock.acquire()
        print('host', self.__host)
        nodes_info = [c for c in Client.nodes_info if not c.get('host') == self.__host]
        print('nodeinfo', nodes_info)
        lock.release()
        if len(nodes_info) > 0:
            index = 0 if len(nodes_info) == 1 else randrange(len(nodes_info))
            try:
                client = Client(nodes_info[index].get('host'), blockchain=self.__blockchain)
                client.start()
                client.join()
                client.send_message('blockchain', disconnect=False)
                print('waiting for blockchain update')
                client.wait()
            except Exception as e:
                print('error => {}'.format(e))
        else:
            print('no nodes')
        self.__blockchain.get_update()

    def start(self):
        try:
            self.__app.run(host=self.__host, port=self.__port, threaded=True)
        except Exception as e:
            print('error from class Server =>', e)

    def start_mining(self):
        self.__mining = True
        self.parent.tab_blockchain.logger.log('Minnage en cours')

    def stop_mining(self):
        self.__mining = False
        self.parent.tab_blockchain.logger.log('Arrêt du minnage')

    def get_balance_from_public_key(self, public_key: bytes):
        return self.__blockchain.get_balance(public_key)

    def get_pending_transactions(self):
        return self.__blockchain.get_pending_transaction()
