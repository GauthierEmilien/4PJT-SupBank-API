import datetime
import json
from Transaction import Transaction
from Block import Block


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 5
        self.pending_transaction = []
        self.reward = 10

    def create_genesis_block(self):
        genesis_block = Block(str(datetime.datetime.now()), "I am the Genesis Block")
        return genesis_block

    def get_last_block(self):
        return self.chain[len(self.chain) - 1]

    def mine_pending_trans(self, miner_reward_address):
        # in reality not all of the pending transaction go into the block the miner gets to pick which one to mine
        new_block = Block(str(datetime.datetime.now()), self.pending_transaction)
        new_block.mine_blocks(self.difficulty)
        new_block.previous_block = self.get_last_block().hash

        print("Previous Block's Hash: " + new_block.previous_block)
        test_chain = []
        for trans in new_block.transactions:
            temp = json.dumps(trans.__dict__, indent=5, separators=(',', ': '))
            test_chain.append(temp)
        print(test_chain)

        self.chain.append(new_block)
        print("Block's Hash: " + new_block.hash)
        print("Block added")

        reward_trans = Transaction("System", miner_reward_address, self.reward)
        self.pending_transaction.append(reward_trans)
        self.pending_transaction = []

    def is_chain_valid(self):
        for x in range(1, len(self.chain)):
            current_block = self.chain[x]
            previous_block = self.chain[x - 1]

            if current_block.previous_block != previous_block.hash:
                return "The Chain is not valid!"
        return "The Chain is valid and secure"

    def create_transaction(self, transaction):
        self.pending_transaction.append(transaction)

    def get_balance(self, wallet_address):
        balance = 0
        for block in self.chain:
            if block.previous_block == "":
                # dont check the first block
                continue
            for transaction in block.transactions:
                if transaction.from_wallet == wallet_address:
                    balance -= transaction.amount
                if transaction.to_wallet == wallet_address:
                    balance += transaction.amount
        return balance
