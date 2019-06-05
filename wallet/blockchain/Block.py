import hashlib
from typing import List

from blockchain.Transaction import Transaction


class Block:
    def __init__(self, timestamp: str, transactions: List[Transaction], hash='', nonce=0, previous_block=''):
        self.__timestamp = timestamp
        self.__transactions: List[Transaction] = transactions
        self.__previous_block = previous_block
        self.__nonce = nonce
        self.__hash: str = hash

    @classmethod
    def from_dict(self, block: dict):  # Return a new Block object from block dict
        transactions: List[Transaction] = [Transaction.from_dict(t) for t in block.get('transactions')]
        return Block(block.get('timestamp'),
                     transactions,
                     block.get('hash'),
                     block.get('nonce'),
                     block.get('previous_block'))

    def calculate_hash(self):  # Calculate block hash with transactions list, timestamp and nonce
        data = (str(self.__transactions) + str(self.__timestamp) + str(self.__nonce)).encode()
        hash = hashlib.sha256(data)
        self.__hash = hash.hexdigest()

    def update_nonce(self):
        self.__nonce += 1

    def get_transactions(self) -> List[Transaction]:
        return self.__transactions

    def add_transaction(self, transaction: Transaction):
        self.__transactions.append(transaction)

    def remove_transaction(self, transaction: Transaction):
        self.__transactions.remove(transaction)
        print('removed transactions', self.__transactions)

    def get_hash(self) -> str:
        return self.__hash

    def get_previous_block(self) -> str:
        return self.__previous_block

    def set_previous_block(self, hash: str):
        self.__previous_block = hash

    def __dict__(self) -> dict:  # return a dict from a Block object
        return {
            'hash':           self.__hash,
            'nonce':          self.__nonce,
            'timestamp':      self.__timestamp,
            'transactions':   [t.__dict__() for t in self.__transactions],
            'previous_block': self.__previous_block
        }
