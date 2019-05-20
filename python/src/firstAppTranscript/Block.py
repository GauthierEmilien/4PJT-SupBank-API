"""
utilisation lib
https://pypi.org/project/eciespy/#description
"""

from typing import List
from firstAppTranscript.Transaction import Transaction
from hashlib import sha256

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
        data = str(self.__previous_hash) + str(self.__timestamp) + str(self.__transactions) + str(self.__nonce)

        return str(sha256(data.encode()))

    """ 
        Starts the mining process on the block. It changes the 'nonce' until the hash
        of the block starts with enough zeros (= difficulty)
    """

    def mine_block(self, difficulty: int) -> None:
        temp = "0"
        while self.__hash.encode('utf-8').hex()[0:difficulty] != '0' * difficulty:
            self.__nonce += 1
            # il sort pas de la
            # leZero = str(b'0').encode('utf-8').hex()
            self.__hash = self.calculate_hash().encode('utf-8').hex()

            print('Block mined:' + self.__hash.encode('utf-8').hex())




    """ 
        Validates all the transactions inside this block (signature + hash) and
        returns true if everything checks out. False if the block is invalid.
    """

    def has_valid_transactions(self) -> bool:
        for tx in self.__transactions:
            if not (tx.isValid()):
                return False
        return True

    def get_hash(self) -> str:
        return self.__hash

    def get_previous_hash(self) -> str:
        return self.__previous_hash

    def get_transactions(self) -> List[Transaction]:
        return self.__transactions
