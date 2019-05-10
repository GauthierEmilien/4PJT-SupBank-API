"""
utilisation lib
https://pypi.org/project/eciespy/#description
"""

from hashlib import sha256
import json
from typing import List
from Transaction import Transaction


class Block:
    def __init__(self, timestamp: int, transactions: List[Transaction], previous_hash: str = ''):
        self.__previous_hash: str = previous_hash
        self.__timestamp = timestamp
        self.__transactions: List[Transaction] = transactions
        self.__nonce = 0
        self.__hash: str = self.calculate_hash()


    """ 
        Returns the SHA256 of this block (by processing all the data stored
        inside this block)
    """
    def calculate_hash(self) -> str:
        return str(sha256(self.__previous_hash + self.__timestamp
                          + json.dumps(self.__transactions) + self.__nonce))


    """ 
        Starts the mining process on the block. It changes the 'nonce' until the hash
        of the block starts with enough zeros (= difficulty)
    """
    def mine_block(self, difficulty: str) -> None:
        while self.__hash[:difficulty] != '0' * difficulty:
            self.__nonce += 1
            self.__hash = self.calculate_hash()
        print('Block mined:' + self.__hash)


    """ 
        Validates all the transactions inside this block (signature + hash) and
        returns true if everything checks out. False if the block is invalid.
    """
    def has_valid_transactions(self) -> bool:
        for tx in self.__transactions:
            if not(tx.isValid()):
                return False
        return True


    def get_hash(self) -> str:
        return self.__hash


    def get_previous_hash(self) -> str:
        return self.__previous_hash


    def get_transactions(self) -> List[Transaction]:
        return self.__transactions
