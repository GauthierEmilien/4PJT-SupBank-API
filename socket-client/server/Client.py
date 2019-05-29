from threading import Thread, RLock
import socketio
from typing import List
from blockchain.Blockchain import Blockchain

lock = RLock()


class Client(Thread):
    nodes_info: List[dict] = []
    connected_nodes: List[dict] = []
    block_is_valid: List[bool] = []

    def __init__(self, server_ip: str, thread_name=None, blockchain: Blockchain = None):
        Thread.__init__(self, name=thread_name)
        self.__sio = socketio.Client()
        self.__server_ip = server_ip  # ip du server ip
        self.__node_ip = ''  # ip du node actuel
        self.__setup_callbacks()
        self.__blockchain = blockchain

    @classmethod
    def send_to_every_nodes(cls, host: str, topic: str, data, disconnect=True, wait=False):
        with lock:
            for node in Client.nodes_info:
                if node.get('host') != host:
                    client = Client(node.get('host'))
                    client.start()
                    client.join()
                    client.send_message(topic, data, disconnect)
                    if wait:
                        client.wait()

    def __setup_callbacks(self):
        self.__sio.on('connect', self.__on_connect)
        self.__sio.on('disconnect', self.__on_disconnect)
        self.__sio.on('nodes', self.__on_nodes)
        self.__sio.on('ip', self.__on_ip)
        self.__sio.on('blockchain', self.__on_blockchain)
        self.__sio.on('block', self.__on_block)

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
        if len(blocks) > len(self.__blockchain.get_blocks()):
            self.__blockchain.update_all(blocks)
        self.__blockchain.get_update()
        self.__disconnect()

    def __on_block(self, is_valid: str):
        print('GET VALIDATION =>', is_valid)
        with lock:
            Client.block_is_valid.append(is_valid)
        self.__disconnect()

    def __disconnect(self):
        self.__sio.disconnect()

    def run(self):
        if self.__server_ip:
            try:
                self.__sio.connect('http://{}:8000'.format(self.__server_ip))
            except Exception as e:
                print('error => {} (server ip : {})'.format(e, self.__server_ip))

    def send_message(self, topic: str, data=None, disconnect: bool = True):
        callback = self.__disconnect if disconnect else None
        self.__sio.emit(topic, data, callback=callback)

    def wait(self):
        self.__sio.wait()

    def get_node_ip(self):
        return self.__node_ip