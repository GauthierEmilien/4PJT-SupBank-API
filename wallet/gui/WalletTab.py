from tkinter import CENTER
from tkinter import E
from tkinter import END
from tkinter import Entry
from tkinter import INSERT
from tkinter import N
from tkinter import S
from tkinter import Text
from tkinter import W
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from wallet.gui.TabFrame import TabFrame


class WalletTab(TabFrame):
    """
    Création du tab "Portefeuille"
    """

    def __init__(self, parent, **args):
        TabFrame.__init__(self, parent, **args)
        self.__amount_transaction = ttk.Entry(self, text='')
        self.__private_wallet_key = Text(self, height=5)
        self.__public_key = Text(self, height=5)
        self.__public_key_destinataire = Text(self, height=5)
        self.initLogger()

        # self.privateKeyGroup()
        self.pulicKeyOfUserGroup()

        self.pulicKeyGroup()
        # self.generateKeys()
        self.walletAmount()
        self.transactionAmount()
        self.transactionButton()

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def privateKeyGroup(self):
        l_private_wallet_key = ttk.Label(self, text='Clé privée', padding=10)
        l_private_wallet_key.grid(row=0, column=0, sticky=N + S + E + W)

        self.__private_wallet_key.grid(row=1, column=0, sticky=N + S + E + W)

        button_open_private = ttk.Button(self, text='Ouvrir une clé privée', width=25,
                                         command=lambda: self.__getPrivateKeyFile(self.__private_wallet_key))
        button_open_private.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)

    def pulicKeyOfUserGroup(self):
        l_public_key = ttk.Label(self, text='Clé public', padding=10)
        l_public_key.grid(row=0, column=0, sticky=N + S + E + W)

        self.__public_key.grid(row=1, column=0, sticky=N + S + E + W)

    def walletAmount(self):
        l_amount_wallet = ttk.Label(self, text='Portefeuille', width=20, anchor=CENTER, padding=10)
        l_amount_wallet.grid(row=0, column=1, columnspan=2, sticky=N + S + E + W)
        amount_wallet = ttk.Label(self, text='200', anchor=CENTER)
        amount_wallet.grid(row=1, column=1, columnspan=2, sticky=N + S + E + W)

    def pulicKeyGroup(self):
        l_public_key = ttk.Label(self, text='Clé public destinataire', padding=10)
        l_public_key.grid(row=3, column=0, sticky=N + S + E + W)

        self.__public_key_destinataire.grid(row=4, column=0, sticky=N + S + E + W)

        # button_open_public = ttk.Button(self, text='Ouvrir une clé public', width=25,
        #                                 command=lambda: self.__getPublicKeyFile(self.__public_key))
        # button_open_public.grid(row=4, column=1, padx=5, pady=5, sticky=N + S + E + W)

    def generateKeys(self):
        # Générer une paire de clé
        l_key_gen = ttk.Label(self, text='Générer une paire de clé', width=20, anchor=CENTER, padding=10)
        l_key_gen.grid(row=0, column=2, sticky=N + S + E + W)

        key_gen = ttk.Button(self, text='Générer une paire de clé', width=25, command=lambda: self.__generateKeys())
        key_gen.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)

    def transactionAmount(self):
        l_amount_transaction = ttk.Label(self, text='Montant de la transaction', anchor=CENTER, padding=10)
        l_amount_transaction.grid(row=3, column=1, columnspan=2, padx=5)
        self.__amount_transaction.grid(row=4, column=1, columnspan=2)

    def transactionButton(self):
        button_valid_transaction = ttk.Button(self, text='Valider la transaction',
                                              command=lambda: self.__createTransaction(self.__private_wallet_key,
                                                                                       self.__public_key_destinataire,
                                                                                       self.__amount_transaction))
        button_valid_transaction.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)

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
        self.logger.success('Création de la transaction')
        self.logger.error('Création de la transaction')
        self.logger.warning('Création de la transaction')
        self.logger.log('Création de la transaction')

    def __generateKeys(self):
        if len(self.__private_wallet_key.get("1.0", END)) > 1024 or len(self.__public_key_destinataire.get("1.0", END)) > 1024:
            if not messagebox.askyesno("Question", "Une clé privée/public existe déjà.\n"
                                                   "Générer quand même une nouvelle paire ?"):
                return
        self.logger.log('Génération de la paire de clé en cours')

        self.__private_wallet_key.delete('1.0', END)
        self.__private_wallet_key.insert(INSERT, 'Clé privée')

        self.__public_key_destinataire.delete('1.0', END)
        self.__public_key_destinataire.insert(INSERT, 'Clé public')

        self.logger.log('Fin de la génération des clés')
