from concurrent.futures import ThreadPoolExecutor
from tkinter import CENTER
from tkinter import DISABLED
from tkinter import E
from tkinter import END
from tkinter import Entry
from tkinter import INSERT
from tkinter import N
from tkinter import NORMAL
from tkinter import S
from tkinter import Text
from tkinter import W
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from Cryptodome.PublicKey import RSA

from wallet.gui.TabFrame import TabFrame


class WalletTab(TabFrame):
    """
    Création du tab "Portefeuille"
    """

    def __init__(self, parent, **args):
        TabFrame.__init__(self, parent.tab_control, **args)
        self.__amount_transaction = ttk.Entry(self, text='')
        self.__private_wallet_key = Text(self, height=5)
        self.__key_object = None
        self.__public_key = Text(self, height=5)
        self.__public_key_destinataire = Text(self, height=5)
        self.init_logger()
        self.parent = parent

        # self.privateKeyGroup()
        self.pulic_key_of_user_group()

        self.pulic_key_target_group()
        # self.generateKeys()
        self.__wallet_amount()
        self.transaction_amount()
        self.transaction_button()

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def pulic_key_of_user_group(self):
        l_public_key = ttk.Label(self, text='Clé public', padding=10)
        l_public_key.grid(row=0, column=0, sticky=N + S + E + W)

        self.__public_key.grid(row=1, column=0, sticky=N + S + E + W)

    def __wallet_amount(self):
        l_amount_wallet = ttk.Label(self, text='Portefeuille', width=20, anchor=CENTER, padding=10)
        l_amount_wallet.grid(row=0, column=1, columnspan=2, sticky=N + S + E + W)

        self.amount_wallet = ttk.Label(self, text=0, anchor=CENTER)
        self.amount_wallet.grid(row=1, column=1, columnspan=2, sticky=N + S + E + W)

    def set_wallet_amount(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            result = executor.submit(self.parent.server.get_wallet_from_public_key, self.__public_key.get('1.0', END))
            amount = result.result()

        self.amount_wallet.setvar('text', amount)

    def pulic_key_target_group(self):
        l_public_key = ttk.Label(self, text='Clé public destinataire', padding=10)
        l_public_key.grid(row=3, column=0, sticky=N + S + E + W)

        self.__public_key_destinataire.grid(row=4, column=0, sticky=N + S + E + W)

        button_open_public = ttk.Button(self, text='Ouvrir une clé public', width=25,
                                        command=lambda: self.__get_public_key_file(self.__public_key_destinataire))
        button_open_public.grid(row=4, column=1, padx=5, pady=5, sticky=N + S + E + W)

    def transaction_amount(self):
        l_amount_transaction = ttk.Label(self, text='Montant de la transaction', anchor=CENTER, padding=10)
        l_amount_transaction.grid(row=3, column=2, padx=5)
        self.__amount_transaction.grid(row=4, column=2)

    def transaction_button(self):
        button_valid_transaction = ttk.Button(self, text='Valider la transaction',
                                              command=lambda: self.__create_transaction(self.__private_wallet_key,
                                                                                        self.__public_key_destinataire,
                                                                                        self.__amount_transaction))
        button_valid_transaction.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)

    def __get_public_key_file(self, entry_field: Text):
        filepath = askopenfilename(title="Ouvrir uneclé public",
                                   filetypes=[('Fichiers pub', '.pub'), ('Tous les fichiers', '*')])
        if filepath:
            with open(filepath) as file:
                value = file.read()
                entry_field.delete('1.0', END)
                entry_field.insert(INSERT, value)

    def __create_transaction(self, private_key: Text, public_key: Text, amount: Entry):
        self.logger.log('Création de la transaction')

        with ThreadPoolExecutor(max_workers=1) as executor:
            result = executor.submit(self.parent.server.create_transaction, private_key.get('1.0', END),
                                     public_key.get('1.0', END), amount.get())
            # result = executor.submit(self.parent.server.create_transaction, self.__key_object,
            #                          public_key.get('1.0', END), amount.get())
            if result:
                self.logger.log('Transaction créée')
            else:
                self.logger.error('Impossible de créer la transaction')

    def set_key_object(self, private_key: str):
        self.key_object = RSA.import_key(private_key)
        self.__public_key.config(state=NORMAL)
        self.__public_key.delete('1.0', END)
        self.__public_key.insert(INSERT, self.key_object.publickey().export_key())
        self.__public_key.config(state=DISABLED)

    # def private_key_group(self):
    #     l_private_wallet_key = ttk.Label(self, text='Clé privée', padding=10)
    #     l_private_wallet_key.grid(row=0, column=0, sticky=N + S + E + W)
    #
    #     self.__private_wallet_key.grid(row=1, column=0, sticky=N + S + E + W)
    #
    #     button_open_private = ttk.Button(self, text='Ouvrir une clé privée', width=25,
    #                                      command=lambda: self.__get_private_key_file(self.__private_wallet_key))
    #     button_open_private.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)

    # def generate_keys(self):
    #     # Générer une paire de clé
    #     l_key_gen = ttk.Label(self, text='Générer une paire de clé', width=20, anchor=CENTER, padding=10)
    #     l_key_gen.grid(row=0, column=2, sticky=N + S + E + W)
    #
    #     key_gen = ttk.Button(self, text='Générer une paire de clé', width=25, command=lambda: self.__generate_keys())
    #     key_gen.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)

    # def __get_private_key_file(self, entry_field: Text):
    #     filepath = askopenfilename(title="Ouvrir une clé privée",
    #                                filetypes=[('Fichiers pem', '.pem'), ('Tous les fichiers', '*')])
    #     if filepath:
    #         with open(filepath) as file:
    #             value = file.read()
    #             entry_field.delete('1.0', END)
    #             entry_field.insert(INSERT, value)

    # def __generate_keys(self):
    #     if len(self.__private_wallet_key.get("1.0", END)) > 1024 or len(
    #             self.__public_key_destinataire.get("1.0", END)) > 1024:
    #         if not messagebox.askyesno("Question", "Une clé privée/public existe déjà.\n"
    #                                                "Générer quand même une nouvelle paire ?"):
    #             return
    #     self.logger.log('Génération de la paire de clé en cours')
    #
    #     self.__private_wallet_key.delete('1.0', END)
    #     self.__private_wallet_key.insert(INSERT, 'Clé privée')
    #
    #     self.__public_key_destinataire.delete('1.0', END)
    #     self.__public_key_destinataire.insert(INSERT, 'Clé public')
    #
    #     self.logger.log('Fin de la génération des clés')
