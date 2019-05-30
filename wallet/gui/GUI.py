from _tkinter import TclError
from tkinter import LEFT
from tkinter import Tk
from tkinter import ttk

from ttkthemes import ThemedStyle

from wallet.gui.AskIp import AskIp
from wallet.gui.BlockchaineTab import BlockchaineTab
from wallet.gui.OptionTab import OptionTab
from wallet.gui.WalletTab import WalletTab


# TODO: Faire passer la popUp au premier plan (dans le cas ou impossible de se connecter)
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
        try:
            self.iconbitmap(r'./ressources/Ph03nyx-Super-Mario-Question-Coin.ico')
        except TclError:
            print('Cannot load the icon')

        self.__tab_control = ttk.Notebook(self)

        tab_control = ttk.Notebook(self)

        # Blockchaine
        self.tab_blockchaine = BlockchaineTab(tab_control)

        tab_control.add(self.tab_blockchaine, text='BlockChain')

        # Wallet
        self.tab_wallet = WalletTab(tab_control)

        tab_control.add(self.tab_wallet, text='Wallet')

        # Options
        self.tab_option = OptionTab(tab_control)

        tab_control.add(self.tab_option, text='Options')

        tab_control.pack(expand=1, fill="both", side=LEFT)

        self.connectIpServer()

    def connectIpServer(self):
        is_connected_to_server_id = False
        if is_connected_to_server_id:
            self.tab_blockchaine.logger.success('Connexion au server IP réussi')
            self.tab_wallet.logger.success('Connexion au server IP réussi')
        else:
            self.serverIp = AskIp(self, 'Impossible de contacter le server IP.\n'
                                        'Entrez l\'ip du server x.x.x.x : ').askvalue()

            if self.serverIp is None:
                self.destroy()
                return

            self.tab_option.setIp(self.serverIp)


fenetre = GUI()
fenetre.mainloop()
