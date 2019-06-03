from _tkinter import TclError
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from threading import Thread
from tkinter import LEFT
from tkinter import Tk
from tkinter import ttk

from ttkthemes import ThemedStyle

from gui.AskIp import AskIp
from gui.AskPrivateKey import AskPrivateKey
from gui.ClickActions import ClickActions
from server.Client import Client
from server.Server import Server
from wallet.gui.BlockchainTab import BlockchainTab
from wallet.gui.OptionTab import OptionTab
from wallet.gui.WalletTab import WalletTab

import asyncio


# TODO: Gerer les bonnes actions sur les boutons
# TODO: Améliorer le responsive
# TODO améliorer les class


class GUI(Tk):
    """
    Création de la fenêtre
    """

    def __init__(self):
        Tk.__init__(self)
        self.style = ThemedStyle(self)
        self.title('XatomeCoin')
        self.configure(bg='white')
        # self.protocol("WM_DELETE_WINDOW", self.on_closing)
        try:
            self.iconbitmap(r'./ressources/Ph03nyx-Super-Mario-Question-Coin.ico')
        except TclError:
            print('Impossible de charger l\'icône')

        self.tab_control = ttk.Notebook(self)

        # Blockchain
        self.tab_blockchain = BlockchainTab(self, self.tab_control)

        self.tab_control.add(self.tab_blockchain, text='BlockChain')

        # Wallet
        self.tab_wallet = WalletTab(self)

        self.tab_control.add(self.tab_wallet, text='Portefeuille')

        # Options
        self.tab_option = OptionTab(self)
        self.tab_option.set_theme_jour()

        self.tab_control.add(self.tab_option, text='Options')

        self.tab_control.pack(expand=1, fill="both", side=LEFT)

        # Right click
        ClickActions().r_clickbinder(self)

        # Config
        self.__server_ip = '127.0.0.1'
        self.__is_server_ip_valid = False

        self.__popup_generate_or_load_private_key()
        if self.private_key is not None:
            self.tab_wallet.set_key_object(self.private_key)
            self.__init_client()
            # TODO : a decommenter
            if self.__server_ip is not None:
                self.__init_server()
                if self.server is not None:
                    self.tab_wallet.set_wallet_amount()

    def __popup_connect_ip_server(self):
        if self.__is_server_ip_valid:
            self.tab_blockchain.logger.success('Connexion au server IP réussi')
            self.tab_wallet.logger.success('Connexion au server IP réussi')
        else:
            self.tab_blockchain.logger.error('Impossible de se connecter au server ip : ' + self.__server_ip)
            self.__server_ip = AskIp(self, title='IP du Server', ask='Impossible de contacter le server IP.\n'
                                                                     'Entrez l\'ip du server x.x.x.x : ').get_result()
            if self.__server_ip is None:
                self.destroy()
                return
            self.tab_option.set_ip(self.__server_ip)

    def __popup_generate_or_load_private_key(self):
        self.private_key = AskPrivateKey(self, title='Clé privée').get_result()
        if self.private_key is None:
            self.destroy()
            return

        self.tab_blockchain.logger.success('Clé privée chargée')
        self.tab_wallet.logger.success('Clé privée chargée')

    def __init_client(self):
        self.client_server_ip = Client(server_ip=self.__server_ip, thread_name='server_ip_connection', parent=self)
        self.client_server_ip.start()
        while not self.__is_server_ip_valid and self.__server_ip is not None:
            with ThreadPoolExecutor(max_workers=1) as executor:
                executor.submit(self.client_server_ip.set_server_ip, self.__server_ip)
                self.client_server_ip.wait()
                f1 = executor.submit(self.client_server_ip.is_connected)
                self.__is_server_ip_valid = f1.result()

            self.__popup_connect_ip_server()

    def __init_server(self):

        def _run(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        with ThreadPoolExecutor(max_workers=1) as executor:
            node_ip = executor.submit(self.client_server_ip.get_node_ip)
            while len(Client.nodes_info) == 0:
                continue

        ioloop = asyncio.new_event_loop()

        self.server = Server(self)

        asyncio.run_coroutine_threadsafe(self.server.launch(node_ip.result(), 8000), loop=ioloop)
        t = Thread(target=partial(_run, ioloop), daemon=True)
        t.start()



        # self.server.launch(node_ip.result(), 8000)
