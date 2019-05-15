from threading import Thread
import socketio

class Client(Thread):

    def __init__(self, server_ip: str, thread_name=None):
        Thread.__init__(self, name=thread_name)
        self.__sio = socketio.Client()
        self.__server_ip = server_ip
        self.__node_ip = ''
        self.__setup_callbacks()


    def run(self):
        if self.__server_ip:
            try:
                self.__sio.connect('http://{}:8000'.format(self.__server_ip))
            except Exception as e:
                print('error =>', e)

    def __setup_callbacks(self):
        self.__sio.on('connect', self.__on_connect)
        self.__sio.on('disconnect', self.__on_disconnect)
        self.__sio.on('nodes', self.__on_nodes)
        self.__sio.on('ip', self.__on_ip)

    def __on_connect(self):
        print('Connected on server with ip {}'.format(self.__server_ip))

    def __on_ip(self, ip):
        self.__node_ip = ip

    def __on_disconnect(self, sid):
        print('disconnected from server with ip {}'.format(self.__server_ip))

    def __on_nodes(self, nodes):
        print(nodes)

    def get_node_ip(self):
        return self.__node_ip