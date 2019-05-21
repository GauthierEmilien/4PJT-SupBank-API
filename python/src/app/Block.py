import hashlib

class Block:
    def __init__(self, time_stamp, transactions, previous_block=''):
        self.time_stamp = time_stamp
        self.transactions = transactions
        self.previous_block = previous_block
        self.nonce = 0
        self.hash = self.calculate_hash(transactions, str(time_stamp), self.nonce)

    def calculate_hash(self, data, time_stamp, nonce):
        data = str(str(data) + str(time_stamp) + str(nonce)).encode()
        hash = hashlib.sha256(data)
        return hash.hexdigest()

    def mine_blocks(self, difficulty):
        difficulty_check = "9" * difficulty
        while self.hash[:difficulty] != difficulty_check:
            self.hash = self.calculate_hash(self.transactions, str(self.time_stamp), self.nonce)
            self.nonce = self.nonce + 1
