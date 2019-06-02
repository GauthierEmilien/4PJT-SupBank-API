from tkinter import DISABLED
from tkinter import SUNKEN
from tkinter import Text
from tkinter import ttk

from blockchain.Transaction import Transaction


class TransactionFrame(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.__x = 0
        self.__y = 0

    def show_transactions(self, transactions: [Transaction]):
        tmp = 0
        for transaction in transactions:
            self.__show(transaction)
            tmp += 1
            self.__y += 1
            if tmp % 2 == 0:
                self.__x += 1
                self.__y = 0

    def __show(self, transaction: Transaction):
        #  FLAT, GROOVE, RAISED, RIDGE, SOLID, SUNKEN
        frame = ttk.Frame(self, padding=10, relief=SUNKEN)
        frame.grid(row=self.__x, column=self.__y)

        emitter = Text(frame, height=3, width=30, padx=5)
        emitter.insert("1.0", transaction.get_from_wallet())
        emitter.configure(state=DISABLED)
        emitter.grid(row=0, column=0)

        receiver = Text(frame, height=3, width=30, padx=5)
        receiver.insert("1.0", transaction.get_to_wallet())
        receiver.configure(state=DISABLED)
        receiver.grid(row=0, column=1)

        amount = ttk.Label(frame, text='Montant de la transaction : ' + str(transaction.get_amount()))
        amount.grid(row=1, column=0, columnspan=2)
