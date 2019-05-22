import hashlib
from Transaction import Transaction
from typing import List

class Block:
    def __init__(self, time_stamp, transactions: List[Transaction], previous_block=''):
        self.__time_stamp = time_stamp
        self.__transactions: List[Transaction] = transactions
        self.__previous_block = previous_block
        self.__nonce = 0
        self.__hash: str = self.__calculate_hash()

    def __calculate_hash(self) -> str:
        data = (str(self.__transactions) + str(self.__time_stamp) + str(self.__nonce)).encode()
        hash = hashlib.sha256(data)
        return hash.hexdigest()

    def mine_blocks(self, difficulty: int) -> None:
        difficulty_check = "0" * difficulty
        while self.__hash[:difficulty] != difficulty_check:
            self.__hash = self.__calculate_hash()
            self.__nonce += 1

    def get_transactions(self) -> List[Transaction]:
        return self.__transactions

    def remove_transaction(self, transaction: Transaction):
        self.__transactions.remove(transaction)
        print('removed transactions', self.__transactions)

    def get_hash(self) -> str:
        return self.__hash

    def get_previous_block(self) -> str:
        return self.__previous_block

    def set_previous_block(self, hash: str):
        self.__previous_block = hash
