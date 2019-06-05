import re
from tkinter import CENTER
from tkinter import DISABLED
from tkinter import END
from tkinter import Entry
from tkinter import INSERT
from tkinter import NORMAL
from tkinter import NSEW
from tkinter import Text
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from Cryptodome.PublicKey import RSA

from gui.TabFrame import TabFrame


class WalletTab(TabFrame):
    """
    Création du tab "Portefeuille"
    """

    def __init__(self, parent, **args):
        TabFrame.__init__(self, parent, **args)
        self.__amount_transaction = ttk.Entry(self, text='')
        self.__private_wallet_key = Text(self, height=5)
        self.__key_object = None
        self.__public_key = Text(self, height=5)
        self.__public_key_destinataire = Text(self, height=5)
        self.init_logger()

        self.pulic_key_of_user_group()

        self.pulic_key_target_group()
        self.__wallet_amount()
        self.transaction_amount()
        self.transaction_button()

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def pulic_key_of_user_group(self):
        l_public_key = ttk.Label(self, text='Clé public', padding=10)
        l_public_key.grid(row=0, column=0, sticky=NSEW)

        self.__public_key.grid(row=1, column=0, sticky=NSEW)

    def __wallet_amount(self):
        l_amount_wallet = ttk.Label(self, text='Portefeuille', width=20, anchor=CENTER, padding=10)
        l_amount_wallet.grid(row=0, column=1, columnspan=2, sticky=NSEW)

        self.amount_wallet = ttk.Label(self, text=0, anchor=CENTER)
        self.amount_wallet.grid(row=1, column=1, columnspan=2, sticky=NSEW)

    def set_wallet_amount(self):
        amount = self.master.master.server.get_balance_from_public_key(self.__key_object.publickey().export_key('DER'))
        self.amount_wallet.configure(text=amount)

    def pulic_key_target_group(self):
        l_public_key = ttk.Label(self, text='Clé public destinataire', padding=10)
        l_public_key.grid(row=3, column=0, sticky=NSEW)

        self.__public_key_destinataire.grid(row=4, column=0, sticky=NSEW)

        button_open_public = ttk.Button(self, text='Ouvrir une clé public', width=25,
                                        command=lambda: self.__get_public_key_file(self.__public_key_destinataire))
        button_open_public.grid(row=4, column=1, padx=5, pady=5, sticky=NSEW)

    def transaction_amount(self):
        l_amount_transaction = ttk.Label(self, text='Montant de la transaction', anchor=CENTER, padding=10)
        l_amount_transaction.grid(row=3, column=2, padx=5)
        self.__amount_transaction.grid(row=4, column=2)

    def transaction_button(self):
        button_valid_transaction = ttk.Button(self, text='Valider la transaction',
                                              command=lambda: self.__create_transaction(self.__public_key_destinataire,
                                                                                        self.__amount_transaction))
        button_valid_transaction.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky=NSEW)

    def __get_public_key_file(self, entry_field: Text):
        filepath = askopenfilename(title="Ouvrir uneclé public",
                                   filetypes=[('Fichiers pub', '.pub'), ('Tous les fichiers', '*')])
        if filepath:
            with open(filepath) as file:
                value = file.read()
                entry_field.delete('1.0', END)
                entry_field.insert(INSERT, value)

    def __create_transaction(self, public_key: Text, amount: Entry):
        str_public_key = public_key.get('1.0', END)
        str_amount = amount.get()

        if self.__is_valid_transaction(str_public_key, str_amount):
            self.logger.log('Création de la transaction')
            self.master.master.server.make_transaction(self.__key_object, str_public_key, int(str_amount))
            self.set_wallet_amount()

    def set_key_object(self, private_key: str):
        self.__key_object = RSA.import_key(private_key)
        self.__public_key.config(state=NORMAL)
        self.__public_key.delete('1.0', END)
        self.__public_key.insert(INSERT, self.__key_object.publickey().export_key())
        self.__public_key.config(state=DISABLED)

    def get_key_object(self) -> RSA.RsaKey:
        return self.__key_object

    def __is_valid_transaction(self, public_key: str, amount: str) -> bool:
        if not self.__is_valid_amount(amount):
            self.logger.error('Champs invalides')
            return False
        if not self.__is_valid_public_key(public_key):
            self.logger.error('Vous ne pouvez pas créer de transaction pour vous-même')
            return False
        if not self.__has_enounght(int(amount)):
            self.logger.error('Vos fonds sont insuffisants')
            return False
        return True

    def __is_valid_amount(self, value: str) -> bool:
        # p = re.compile(r'^\d+([.,]\d+)?$')
        p = re.compile(r'^\d$')
        if p.match(value):
            return int(value) > 0
        return False

    def __has_enounght(self, value: int) -> bool:
        return value <= self.amount_wallet['text']

    def __is_valid_public_key(self, value: str) -> bool:
        try:
            to_pub_key = RSA.import_key(value).export_key('DER')
            return to_pub_key != self.__key_object.publickey().export_key('DER')
        except Exception:
            return False
