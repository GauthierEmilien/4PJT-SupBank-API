import re
from _tkinter import TclError
from tkinter import LEFT
from tkinter import Tk
from tkinter import simpledialog
from tkinter import ttk

from gui.BlockchaineTab import BlockchaineTab
from gui.WalletTab import WalletTab


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

        tab_control.pack(expand=1, fill="both", side=LEFT)

        self.connectIpServer()

    def connectIpServer(self):
        is_connected_to_server_id = False
        if is_connected_to_server_id:
            self.tab_blockchaine.logger.success('Connexion au server IP réussi')
            self.tab_wallet.logger.success('Connexion au server IP réussi')
        else:
            # Popup window
            block_request_top = Tk.winfo_toplevel(self)
            block_request_top.title("Blocked fields")

            block_request_top.withdraw()

            entry_block = simpledialog.askstring("Blocked fields",
                                                 'Impossible de contacter le server IP.\n'
                                                 'Entrez l\'ip du server x.x.x.x : ',
                                                 parent=block_request_top)
            block_request_top.iconify()
            block_request_top.deiconify()
            p = re.compile('(\d{1,3}\.){3}\d{1,3}')
            if not entry_block or not p.match(entry_block):
                self.connectIpServer()


fenetre = GUI()
fenetre.mainloop()
