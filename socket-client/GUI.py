import re
from _tkinter import TclError
from tkinter import LEFT
from tkinter import Tk
from tkinter import simpledialog
from tkinter import ttk

from gui.BlockchaineTab import BlockchaineTab
from gui.OptionTab import OptionTab
from gui.WalletTab import WalletTab

# import blockchain.Client
# import blockchain.global_var


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

        # Options
        self.tab_option = OptionTab(tab_control)

        tab_control.add(self.tab_option, text='Options')

        tab_control.pack(expand=1, fill="both", side=LEFT)

        self.__entry_block = ''

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

            self.__entry_block = simpledialog.askstring("Blocked fields",
                                                 'Impossible de contacter le server IP.\n'
                                                 'Entrez l\'ip du server x.x.x.x : ',
                                                 parent=block_request_top)
            block_request_top.iconify()
            block_request_top.deiconify()
            p = re.compile(r'(\d{1,3}\.){3}\d{1,3}')

            if self.__entry_block is None:
                self.destroy()
                return

            if not p.match(self.__entry_block):
                self.connectIpServer()

    def get_entry_point(self):
        return self.__entry_block


def sup():
    while True:
        print("n")

def init_server():
    import blockchain.Client
    import blockchain.global_var
    print(fenetre.get_entry_point())


fenetre = GUI()
print('popup')
fenetre.after(0, init_server())
fenetre.mainloop()

# t = Thread(target=mainGui)
# t.start()

print("coucou")