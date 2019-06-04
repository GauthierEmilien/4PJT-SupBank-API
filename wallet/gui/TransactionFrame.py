from tkinter import DISABLED
from tkinter import E
from tkinter import Text
from tkinter import W
from tkinter import ttk

from blockchain.Transaction import Transaction
from gui.TextAndScrollBar import TextAndScrollBar


class TransactionFrame(ttk.Frame):

    def __init__(self, parent, **args):
        ttk.Frame.__init__(self, parent, **args)
        self.__transaction_text = TextAndScrollBar(self, wrap="char", borderwidth=0, highlightthickness=0,
                                                   state="disabled")
        self.__transaction_text.pack(fill="both", expand=True)
        self.__transactions_boxes = []

    def show_transactions(self, transactions: [Transaction]):
        for transaction in transactions:
            box = self.__add_transaction_box(transaction)
            self.__transactions_boxes.append(box)
            self.__transaction_text.configure(state="normal")
            self.__transaction_text.window_create("end", window=box)
            self.__transaction_text.configure(state="disabled")

    def __add_transaction_box(self, transaction: Transaction):
        #  FLAT, GROOVE, RAISED, RIDGE, SOLID, SUNKEN
        frame = ttk.Frame(self.__transaction_text, relief="sunken", padding=5)

        l_from = ttk.Label(frame, text='Expediteur : ')
        l_from.grid(row=0, column=0, sticky=W)
        emitter = Text(frame, height=3, padx=5, width=45)
        print('type : ', type(transaction.get_from_wallet()))
        emitter.insert("1.0", transaction.get_from_wallet())
        emitter.configure(state=DISABLED)
        emitter.grid(row=1, column=0)

        amount = ttk.Label(frame, text='Destinataire : ')
        amount.grid(row=2, column=0, sticky=W)
        receiver = Text(frame, height=3, padx=5, width=45)
        print('type : ', type(transaction.get_to_wallet()))
        receiver.insert("1.0", transaction.get_to_wallet())
        receiver.configure(state=DISABLED)
        receiver.grid(row=3, column=0)

        amount = ttk.Label(frame, text='Montant de la transaction : ' + str(transaction.get_amount()),
                           font=('Arial', 12, 'bold'))
        amount.grid(row=4, column=0, columnspan=2, sticky=E)
        return frame
