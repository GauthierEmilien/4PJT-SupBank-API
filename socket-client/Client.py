from threading import Thread, RLock
import socketio
from typing import List

lock = RLock()


class Client(Thread):
    nodes_info: List[dict] = []
    connected_nodes: List[dict] = []

    def __init__(self, server_ip: str, thread_name=None, is_node=False):
        Thread.__init__(self, name=thread_name)
        self.__sio = socketio.Client()
        self.__server_ip = server_ip    # ip du server ip
        self.__node_ip = ''             # ip du node actuel
        self.__setup_callbacks()
        self.__is_node = is_node

    def run(self):
        if self.__server_ip:
            try:
                self.__sio.connect('http://{}:8000'.format(self.__server_ip))
                if self.__is_node:
                    print('emit test')
                    self.__sio.emit('test', 'salut salut ({})'.format(self.__server_ip), callback=self.__disconnect)
            except Exception as e:
                print('error => {} (server ip : {})'.format(e, self.__server_ip))

    def __disconnect(self):
        self.__sio.disconnect()

    def __setup_callbacks(self):
        self.__sio.on('connect', self.__on_connect)
        self.__sio.on('disconnect', self.__on_disconnect)
        self.__sio.on('nodes', self.__on_nodes)
        self.__sio.on('ip', self.__on_ip)

    def __on_connect(self):
        print('\nCONNECT TO => {}'.format(self.__server_ip))
        """Pour tester l'envoie d'un message a d'autres noeuds"""
        # self.__sio.emit('test', 'bonjour')

    def __on_ip(self, ip):
        self.__node_ip = ip

    def __on_disconnect(self):
        print('\nDISCONNECT FROM => {}'.format(self.__server_ip))

    def __on_nodes(self, nodes):
        with lock:
            Client.nodes_info = nodes
            print('\nNODES =>', Client.nodes_info)

        """
        Code a utiliser au cas ou un noeud doit envoyer un message a tous les autres neouds
        permet de bloquer l'essaie de connexion au noeuds qui sont deja connectes sur celui la
        """
        # for node in Client.nodes_info:
        #     if node.get('host') != self.__node_ip and next(
        #             (i for i, d in enumerate(Client.connected_nodes) if node.get('host') in d), False):
        #         co = Client(node.get('host'), is_node=True)
        #         co.start()
        #         co.join()

    def get_node_ip(self):
        return self.__node_ip
