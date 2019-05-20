from firstAppTranscript.Block import Block
from firstAppTranscript.Transaction import Transaction
from typing import List
from datetime import datetime
from Crypto.PublicKey.RSA import RsaKey
from Crypto.PublicKey import RSA
import time
import json


class Blockchain:
    def __init__(self):
        self.__chain: List[Block] = [self.create_genesis_block()]
        self.__difficulty = 2
        self.__pendingTransactions: List[Transaction] = []
        self.__miningReward = 100


    def create_genesis_block(self) -> Block:
        return Block(int(round(datetime(2017, 1, 1).timestamp() * 1000)), [], '0')


    """
    Returns the latest block on our chain. Useful when you want to create a
    new Block and you need the hash of the previous Block.
    """
    def get_latest_block(self) -> Block:
        return self.__chain[-1]


    """
    Takes all the pending transactions, puts them in a Block and starts the
    mining process. It also adds a transaction to send the mining reward to
    the given address.
    """
    def mine_pending_transaction(self, mining_reward_address: RsaKey) -> None:
        rewardTx = Transaction(RSA.generate(1024).publickey(), mining_reward_address, self.__miningReward)
        self.__pendingTransactions.append(rewardTx)

        block = Block(int(round(time.time() * 1000)),
                      self.__pendingTransactions, self.get_latest_block().get_hash())

        block.mine_block(self.__difficulty)
        print('block successfully mined')

        self.__chain.append(block)
        self.__pendingTransactions = []


    """
    Add a new transaction to the list of pending transactions (to be added
    next time the mining process starts). This verifies that the given
    transaction is properly signed.
    """
    def add_transaction(self, transaction: Transaction) -> None:
        if not transaction.get_from_address().export_key().decode() \
                or not transaction.get_to_address().export_key().decode():
            raise Exception('Transaction must include from and to address')

        # if (not transaction.is_valid()):
        #     raise Exception('Cannot add invalid transaction to chain')

        self.__pendingTransactions.append(transaction)


    """
    Returns the balance of a given wallet address.
    """
    def get_balance_of_address(self, address: str) -> int:
        balance = 0

        for block in self.__chain:
            for trans in block.get_transactions():
                if trans.get_from_address() == address:
                    balance -= trans.get_amount()

                if trans.get_to_address() == address:
                    balance += trans.get_amount()

        return balance


    """
    Returns a list of all transactions that happened
    to and from the given wallet address.
    """
    def get_all_transactions_for_wallet(self, address) -> List[Transaction]:
        txs: List[Transaction] = []

        for block in self.__chain:
            for tx in block.get_transactions():
                if tx.get_from_address() == address or tx.get_to_address() == address:
                    txs.append(tx)

        return txs


    """
    Loops over all the blocks in the chain and verify if they are properly
    linked together and nobody has tampered with the hashes. By checking
    the blocks it also verifies the (signed) transactions inside of them.
    """
    def is_chain_valid(self) -> bool:
        realGenesis = json.dumps(self.create_genesis_block())

        if realGenesis != json.dumps(self.__chain[0]):
            return False

        for i in range(1, len(self.__chain)):
            currentBlock = self.__chain[i]
            previousBlock = self.__chain[i - 1]

            if not currentBlock.has_valid_transactions() \
                    or currentBlock.get_hash() != currentBlock.calculate_hash() \
                    or currentBlock.get_previous_hash() != previousBlock.calculate_hash():
                return False

        return False
