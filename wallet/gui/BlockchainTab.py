from tkinter import CENTER
from tkinter import E
from tkinter import N
from tkinter import S
from tkinter import W
from tkinter import ttk

from blockchain.Transaction import Transaction
from gui.MiningButton import MiningButton
from gui.TabFrame import TabFrame
from gui.TextAndScrollBar import TextAndScrollBar
from gui.TransactionFrame import TransactionFrame


class BlockchainTab(TabFrame):
    """
    Création du tab "blockchain"
    """

    def __init__(self, parent, **args):
        TabFrame.__init__(self, parent, **args)
        self.pack()
        self.init_logger()

        self.__mining_actions()
        self.pending_transactions()
        # self.generatedBlocks()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure(2, weight=5)

    def __mining_actions(self):
        self.__buttonStartMining = MiningButton(self, text="Commencer à miner",
                                                command=lambda: self.__button_start_mining_action())
        self.__buttonStartMining.show()
        self.__buttonStopMining = MiningButton(self, text="Arrêter de miner",
                                               command=lambda: self.__button_stop_mining_action())

    def __button_start_mining_action(self):
        # self.logger.log('Mining in progress')
        # with ThreadPoolExecutor(max_workers=1) as executor:
        #     result = executor.submit(self.parent.server.start_mining)
            # if result.result() is str:
            #     self.logger.log('Minnage en cours')
            # else:
            #     self.logger.warning('Impossible de miner')
        self.master.master.server.start_mining()
        self.__buttonStartMining.hide()
        self.__buttonStopMining.show()

    def __button_stop_mining_action(self):
        # self.logger.log('Stop Mining')
        # with ThreadPoolExecutor(max_workers=1) as executor:
        #     result = executor.submit(self.parent.server.stop_mining)
        self.master.master.server.stop_mining()
        self.__buttonStopMining.hide()
        self.__buttonStartMining.show()

    def pending_transactions(self):
        label_pending = ttk.Label(self, text='Transactions en attente', anchor=CENTER, padding=10)
        label_pending.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky=N + S + E + W)
        transactions = []
        transactions.append(Transaction('1231232', b'from: blablabla', b'to: blablabla', 666))
        transactions.append(Transaction('1234655', b'from: blablabla', b'to: blablabla', 666))
        transactions.append(Transaction('1235789', b'from: blablabla', b'to: blablabla', 666))
        transactions_frame = TransactionFrame(self)
        transactions_frame.show_transactions(transactions)
        transactions_frame.grid(row=3, column=0, rowspan=6, columnspan=4, padx=5, pady=5, sticky=N + S + E + W)

        # pending_transactions_frame.grid(row=3, column=0, rowspan=6, columnspan=4, padx=5, pady=5, sticky=N + S + E + W)
        # pending_transactions = TextAndScrollBar(pending_transactions_frame, state='disabled')

    def __generated_blocks(self):
        label_blocks = ttk.Label(self, text='Blocks généré', anchor=CENTER, padding=10)
        label_blocks.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        generated_blocks_frame = ttk.Frame(self)
        generated_blocks_frame.grid(row=3, column=2, rowspan=6, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
        generated_blocks = TextAndScrollBar(generated_blocks_frame, state='disabled')
