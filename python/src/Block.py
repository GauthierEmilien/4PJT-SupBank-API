"""
utilisation lib
https://pypi.org/project/eciespy/#description
"""

import hashlib
import json
SHA256 = hashlib.sha256()


class Block:
    def __init__(self, timestamp, transactions, previous_hash=''):
        self.__previous_hash = previous_hash
        self.__timestamp = timestamp
        self.__transactions = transactions
        self.__nonce = 0
        self.__hash = self.calculate_hash()

    """ 
        Returns the SHA256 of this block (by processing all the data stored
        inside this block)
        @returns {string}
    """
    def calculate_hash(self):
        return str(SHA256(self.__previous_hash + self.__timestamp + json.dumps(self.__transactions) + self.__nonce))

    """ 
        Starts the mining process on the block. It changes the 'nonce' until the hash
        of the block starts with enough zeros (= difficulty)
        @param {number} difficulty
    """
    def mine_block(self, difficulty):
        while self.__hash[:difficulty] != '0' * difficulty:
            self.__nonce += 1
            self.__hash = self.calculate_hash()
        print('Block mined:' + self.__hash)

    """ 
        Validates all the transactions inside this block (signature + hash) and
        returns true if everything checks out. False if the block is invalid.
        @returns {boolean}
    """
    def has_valid_transactions(self):
        for tx in self.__transactions:
            if not(tx.isValid()):
                return False
        return True

