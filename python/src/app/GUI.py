from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename


# TODO: Gerer les bonnes actions sur les boutons
# TODO: Améliorer le responsive
# TODO: Changer les couleurs de l'interface

class TextAndScrollBar(Text):

    def __init__(self, parent, *args, **kw):
        Text.__init__(self, parent, *args, **kw)
        scrollbar = Scrollbar(parent)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.configure(yscrollcommand=scrollbar.set)
        self.pack(fill=BOTH)


class Logger(Frame):

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.__loggerText = TextAndScrollBar(self, state='disabled', height=8)
        self.__loggerText.tag_config("log", foreground="black")
        self.__loggerText.tag_config("warning", foreground="orange")
        self.__loggerText.tag_config("error", foreground="red")
        # self.grid(row=9, column=0, columnspan=3, sticky=N + S + E + W)

    def __commonLog(self, log: str, color: str):
        self.__loggerText.config(state=NORMAL)
        self.__loggerText.insert(END, log + '\n', color)
        self.__loggerText.config(state=DISABLED)

    def log(self, log: str):
        self.__commonLog(log, 'log')

    def warning(self, log: str):
        self.__commonLog(log, 'warning')

    def error(self, log: str):
        self.__commonLog(log, 'error')


class MiningButton(Button):

    def __init__(self, parent, **args):
        Button.__init__(self, parent, **args)

    def show(self):
        self.grid(row=0, column=0, rowspan=2, columnspan=4, padx=5, pady=5, sticky=N + S + E + W)

    def hide(self):
        self.grid_forget()


class MainWindow(Tk):
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

    def getTabControl(self):
        return self.__tab_control


class TabFrame(Frame):

    def __init__(self, parent, **args):
        Frame.__init__(self, parent, **args)

    def initLogger(self):
        # Mining logs
        self.logger = Logger(self)
        self.logger.grid(row=10, column=0, columnspan=4, sticky=S + E + W)
        self.grid_rowconfigure(10, weight=2)


class BlockchaineTab(TabFrame):
    """
    Création du tab "blockchaine"
    """

    def __init__(self, parent, **args):
        TabFrame.__init__(self, parent, **args)
        self.pack()
        self.initLogger()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(2, weight=5)

    def miningActions(self):
        self.__buttonStartMining = MiningButton(self, text="Start mining",
                                                command=lambda: self.__buttonStartMiningAction(), height=2)
        self.__buttonStartMining.show()
        self.__buttonStopMining = MiningButton(tab_blockchaine, text="Stop mining",
                                               command=lambda: self.__buttonStopMiningAction(), height=2)

    def __buttonStartMiningAction(self):
        self.logger.log('Mining in progress')
        self.__buttonStartMining.hide()
        self.__buttonStopMining.show()

    def __buttonStopMiningAction(self):
        self.logger.log('Stop Mining')
        self.__buttonStopMining.hide()
        self.__buttonStartMining.show()

    def pendingTransactions(self):
        label_pending = Label(self, text='Pending transaction', background='red', anchor=CENTER)
        label_pending.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        pending_transactions_frame = Frame(self)
        pending_transactions_frame.grid(row=3, column=0, rowspan=6, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        pending_transactions = TextAndScrollBar(pending_transactions_frame, state='disabled')

    def generatedBlocks(self):
        label_blocks = Label(self, text='Block généré', background='red', anchor=CENTER)
        label_blocks.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        generated_blocks_frame = Frame(self)
        generated_blocks_frame.grid(row=3, column=2, rowspan=6, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        generated_blocks = TextAndScrollBar(generated_blocks_frame, state='disabled')


class WalletTab(TabFrame):
    """
    Création du tab "Portefeuille"
    """

    def __init__(self, parent, **args):
        TabFrame.__init__(self, parent, **args)
        self.__amount_transaction = Entry(self, text='')
        self.__private_wallet_key = Text(self, height=5)
        self    .__public_key = Text(self, height=5)
        self.initLogger()

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def privateKeyGroup(self):
        l_private_wallet_key = Label(self, text='Clé privée')
        l_private_wallet_key.grid(row=0, column=0, sticky=N + S + E + W)

        self.__private_wallet_key.grid(row=1, column=0, sticky=N + S + E + W)

        button_open_private = Button(self, text='Ouvrir une clé privée', width=25,
                                     command=lambda: self.__getPrivateKeyFile(self.__private_wallet_key))
        button_open_private.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)

    def pulicKeyGroup(self):
        l_public_key = Label(self, text='Clé public destinataire')
        l_public_key.grid(row=3, column=0, sticky=N + S + E + W)

        self.__public_key.grid(row=4, column=0, sticky=N + S + E + W)

        button_open_public = Button(self, text='Ouvrir une clé public', width=25,
                                    command=lambda: self.__getPublicKeyFile(self.__public_key))
        button_open_public.grid(row=4, column=1, padx=5, pady=5, sticky=N + S + E + W)

    def generateKeys(self):
        # Générer une paire de clé
        l_key_gen = Label(self, text='Générer une paire de clé', width=20)
        l_key_gen.grid(row=0, column=2, sticky=N + S + E + W)

        key_gen = Button(self, text='Générer une paire de clé', width=25, command=lambda: self.__generateKeys())
        key_gen.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)

    def amount(self):
        l_amount_transaction = Label(self, text='Montant de la transaction')
        l_amount_transaction.grid(row=6, column=0, sticky=N + S + E + W)
        self.__amount_transaction.grid(row=7, column=0, sticky=N + S + E + W)

    def transactionButton(self):
        button_valid_transaction = Button(self, text='Valider la transaction', height=2,
                                          command=lambda: self.__createTransaction(self.__private_wallet_key,
                                                                                   self.__public_key,
                                                                                   self.__amount_transaction))
        button_valid_transaction.grid(row=7, column=1, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)

    def __getPrivateKeyFile(self, entry_field: Text):
        filepath = askopenfilename(title="Ouvrir une clé privée",
                                   filetypes=[('pem files', '.pem'), ('all files', '*')])
        if filepath:
            with open(filepath) as file:
                value = file.read()
                entry_field.delete('1.0', END)
                entry_field.insert(INSERT, value)

    def __getPublicKeyFile(self, entry_field: Text):
        filepath = askopenfilename(title="Ouvrir uneclé public",
                                   filetypes=[('pub files', '.pub'), ('all files', '*')])
        if filepath:
            with open(filepath) as file:
                value = file.read()
                entry_field.delete('1.0', END)
                entry_field.insert(INSERT, value)

    def __createTransaction(self, private_key: Text, public_key: Text, amount: Entry):
        self.logger.log('Création de la transaction')
        self.logger.error('Création de la transaction')
        self.logger.warning('Création de la transaction')
        self.logger.log('Création de la transaction')

    def __generateKeys(self):
        if len(self.__private_wallet_key.get("1.0", END)) > 1024 or len(self.__public_key.get("1.0", END)) > 1024:
            if not messagebox.askyesno("Question", "Une clé privée/public existe déjà.\n"
                                                   "Générer quand même une nouvelle paire ?"):
                return
        self.logger.log('Génération de la paire de clé en cours')

        self.__private_wallet_key.delete('1.0', END)
        self.__private_wallet_key.insert(INSERT, 'Clé privée')

        self.__public_key.delete('1.0', END)
        self.__public_key.insert(INSERT, 'Clé public')

        self.logger.log('Fin de la génération des clés')


fenetre = MainWindow()
tab_control = ttk.Notebook(fenetre)

# Blockchaine
tab_blockchaine = BlockchaineTab(tab_control)
tab_blockchaine.miningActions()
tab_blockchaine.pendingTransactions()
tab_blockchaine.generatedBlocks()

tab_control.add(tab_blockchaine, text='BlockChain')

# Wallet
tab_wallet = WalletTab(tab_control)
tab_wallet.privateKeyGroup()
tab_wallet.pulicKeyGroup()
tab_wallet.generateKeys()
tab_wallet.amount()
tab_wallet.transactionButton()

tab_control.add(tab_wallet, text='Wallet')

tab_control.pack(expand=1, fill="both", side=LEFT)

# def connectIpServer():
#     is_connected_to_server_id = False
#     if is_connected_to_server_id:
#         # mining_logger.log('Connexion au server IP réussi')
#         wallet_logger.log('Connexion au server IP réussi')
#     else:
#         # mining_logger.warning('impossible de se connecter au server IP')
#         wallet_logger.warning('impossible de se connecter au server IP')
#         simpledialog.askstring("Input", 'Impossible de contacter le server IP.\nEntrez l\'ip du server x.x.x.x : ',
#                                parent=fenetre)


# connectIpServer()

fenetre.mainloop()
