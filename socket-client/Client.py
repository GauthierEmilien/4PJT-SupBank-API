from threading import Thread, RLock
import socketio
from typing import List
from Transaction import Transaction
from Blockchain import Blockchain
from global_var import xatome_money

lock = RLock()


class Client(Thread):
    nodes_info: List[dict] = []
    connected_nodes: List[dict] = []

    def __init__(self, server_ip: str, thread_name=None):
        Thread.__init__(self, name=thread_name)
        self.__sio = socketio.Client()
        self.__server_ip = server_ip  # ip du server ip
        self.__node_ip = ''  # ip du node actuel
        self.__setup_callbacks()

    def __setup_callbacks(self):
        self.__sio.on('connect', self.__on_connect)
        self.__sio.on('disconnect', self.__on_disconnect)
        self.__sio.on('nodes', self.__on_nodes)
        self.__sio.on('ip', self.__on_ip)
        self.__sio.on('blockchain', self.__on_blockchain)

    def __on_connect(self):
        print('\nCONNECT TO => {}'.format(self.__server_ip))

    def __on_disconnect(self):
        print('\nDISCONNECT FROM => {}'.format(self.__server_ip))

    def __on_nodes(self, nodes):
        with lock:
            Client.nodes_info = nodes
            print('\nNODES =>', Client.nodes_info)

    def __on_ip(self, ip):
        self.__node_ip = ip

    def __on_blockchain(self, blocks: List[dict]):
        print('on blockchain')
        Blockchain.update_all(blocks)
        xatome_money.get_update()
        self.__disconnect()

    def __disconnect(self):
        self.__sio.disconnect()

    def run(self):
        if self.__server_ip:
            try:
                self.__sio.connect('http://{}:8000'.format(self.__server_ip))
            except Exception as e:
                print('error => {} (server ip : {})'.format(e, self.__server_ip))

    def send_transaction(self, transaction: Transaction):
        print('\nSEND TRANSACTION => {}'.format(transaction.__dict__()))
        self.__sio.emit('transaction', transaction.__dict__(), callback=self.__disconnect)

    def ask_for_blockchain(self):
        print('\nASK BLOCKCHAIN')
        self.__sio.emit('blockchain')

    def wait(self):
        self.__sio.wait()

    def get_node_ip(self):
        return self.__node_ip
