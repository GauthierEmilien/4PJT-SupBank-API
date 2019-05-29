from tkinter import CENTER
from tkinter import E
from tkinter import N
from tkinter import S
from tkinter import W
from tkinter import ttk

from wallet.gui.MiningButton import MiningButton
from wallet.gui.TabFrame import TabFrame
from wallet.gui.TextAndScrollBar import TextAndScrollBar


class BlockchaineTab(TabFrame):
    """
    Création du tab "blockchaine"
    """

    def __init__(self, parent, **args):
        TabFrame.__init__(self, parent, **args)
        self.pack()
        self.initLogger()

        self.miningActions()
        self.pendingTransactions()
        self.generatedBlocks()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(2, weight=5)

    def miningActions(self):
        self.__buttonStartMining = MiningButton(self, text="Start mining",
                                                command=lambda: self.__buttonStartMiningAction())
        self.__buttonStartMining.show()
        self.__buttonStopMining = MiningButton(self, text="Stop mining",
                                               command=lambda: self.__buttonStopMiningAction())

    def __buttonStartMiningAction(self):
        self.logger.log('Mining in progress')
        self.__buttonStartMining.hide()
        self.__buttonStopMining.show()

    def __buttonStopMiningAction(self):
        self.logger.log('Stop Mining')
        self.__buttonStopMining.hide()
        self.__buttonStartMining.show()

    def pendingTransactions(self):
        label_pending = ttk.Label(self, text='Pending transaction', background='red', anchor=CENTER)
        label_pending.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        pending_transactions_frame = ttk.Frame(self)
        pending_transactions_frame.grid(row=3, column=0, rowspan=6, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        pending_transactions = TextAndScrollBar(pending_transactions_frame, state='disabled')

    def generatedBlocks(self):
        label_blocks = ttk.Label(self, text='Block généré', background='red', anchor=CENTER)
        label_blocks.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        generated_blocks_frame = ttk.Frame(self)
        generated_blocks_frame.grid(row=3, column=2, rowspan=6, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        generated_blocks = TextAndScrollBar(generated_blocks_frame, state='disabled')