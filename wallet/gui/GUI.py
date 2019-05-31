from _tkinter import TclError
from concurrent.futures import ThreadPoolExecutor
from tkinter import LEFT
from tkinter import Tk
from tkinter import ttk

from ttkthemes import ThemedStyle

from gui.AskIp import AskIp
from gui.AskPrivateKey import AskPrivateKey
from server.Client import Client
from server.Server import Server
from wallet.gui.BlockchaineTab import BlockchaineTab
from wallet.gui.OptionTab import OptionTab
from wallet.gui.WalletTab import WalletTab


# TODO: Gerer les bonnes actions sur les boutons
# TODO: Améliorer le responsive
# TODO: Changer les couleurs de l'interface
# TODO améliorer les class


class GUI(Tk):
    """
    Création de la fenêtre
    """

    def __init__(self):
        Tk.__init__(self)
        style = ThemedStyle(self)
        style.set_theme("arc")
        # style.set_theme("equilux")
        self.title('XatomeCoin')
        self.configure(bg='white')
        # self.protocol("WM_DELETE_WINDOW", self.on_closing)
        try:
            self.iconbitmap(r'./ressources/Ph03nyx-Super-Mario-Question-Coin.ico')
        except TclError:
            print('Cannot load the icon')

        self.__tab_control = ttk.Notebook(self)

        tab_control = ttk.Notebook(self)

        # Blockchaine
        self.tab_blockchaine = BlockchaineTab(self, tab_control)

        tab_control.add(self.tab_blockchaine, text='BlockChain')

        # Wallet
        self.tab_wallet = WalletTab(tab_control)

        tab_control.add(self.tab_wallet, text='Wallet')

        # Options
        self.tab_option = OptionTab(tab_control)

        tab_control.add(self.tab_option, text='Options')

        tab_control.pack(expand=1, fill="both", side=LEFT)

        self.serverIp = '127.0.0.1'
        self.is_server_ip_valid = False

        self.generate_or_load_private_key()
        if self.private_key is not None:
            self.initClient()
            if self.serverIp is not None:
                self.initServer()

    def connectIpServer(self):
        if self.is_server_ip_valid:
            self.tab_blockchaine.logger.success('Connexion au server IP réussi')
            self.tab_wallet.logger.success('Connexion au server IP réussi')
        else:
            self.tab_blockchaine.logger.error('Impossible de se connecter au server ip : ' + self.serverIp)
            self.serverIp = AskIp(self, title='IP du Server', ask='Impossible de contacter le server IP.\n'
                                                                  'Entrez l\'ip du server x.x.x.x : ').askvalue()
            if self.serverIp is None:
                self.destroy()
                return
            self.tab_option.setIp(self.serverIp)

    def generate_or_load_private_key(self):
        self.private_key = AskPrivateKey(self, title='Clé privée').askvalue()
        if self.private_key is None:
            self.destroy()
            return

        self.tab_blockchaine.logger.success('Clé privée chargée')
        self.tab_wallet.logger.success('Clé privée chargée')

    def initClient(self):
        # TODO: a tester avec VM
        self.client_server_ip = Client(server_ip=self.serverIp, thread_name='server_ip_connection', parent=self)
        self.client_server_ip.start()
        while not self.is_server_ip_valid and self.serverIp is not None:
            with ThreadPoolExecutor(max_workers=1) as executor:
                f1 = executor.submit(self.client_server_ip.is_connected)
                self.is_server_ip_valid = f1.result()

            self.connectIpServer()

    def initServer(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            node_ip = executor.submit(self.client_server_ip.get_node_ip)
        self.server = Server(self)
        self.server.start(node_ip, 8000)
