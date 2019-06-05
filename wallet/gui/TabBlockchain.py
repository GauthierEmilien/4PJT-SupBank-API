from tkinter import NSEW
from tkinter import ttk
from typing import List

from blockchain.Transaction import Transaction
from gui.TabFrame import TabFrame
from gui.TransactionFrame import TransactionFrame


class BlockchainTab(TabFrame):
    """
    Création du tab "blockchain"
    """

    def __init__(self, parent, **args):
        TabFrame.__init__(self, parent, **args)
        self.pack(fill='both')

        self.init_logger()

        self.__mining_actions()
        self.pending_transactions()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        for y in range(self.grid_size()[1]):
            self.grid_rowconfigure(y, weight=1)

    def __mining_actions(self):
        self.__buttonStartMining = ttk.Button(self, text="Commencer à miner",
                                              command=lambda: self.__button_start_mining_action())
        self.__buttonStartMining.grid(row=0, column=0, rowspan=2, columnspan=3, padx=5, pady=5, sticky=NSEW)
        self.__buttonStopMining = ttk.Button(self, text="Arrêter de miner",
                                             command=lambda: self.__button_stop_mining_action())
        self.__buttonStopMining.grid(row=0, column=0, rowspan=2, columnspan=3, padx=5, pady=5, sticky=NSEW)
        self.__buttonStopMining.grid_remove()

    def __button_start_mining_action(self):
        self.master.master.server.start_mining()
        self.__buttonStartMining.grid_remove()
        self.__buttonStopMining.grid()

    def __button_stop_mining_action(self):
        self.master.master.server.stop_mining()
        self.__buttonStopMining.grid_remove()
        self.__buttonStartMining.grid()

    def pending_transactions(self):
        self.__transactions_frame = TransactionFrame(self)
        self.__transactions_frame.grid(row=2, column=0, columnspan=3, rowspan=8, padx=5, pady=5, sticky=NSEW)

    def set_pending_transactions(self, transactions: List[Transaction]):
        self.__transactions_frame.show_transactions(transactions)
