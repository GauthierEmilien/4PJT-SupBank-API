import datetime
import json
from Transaction import Transaction
from Block import Block
from typing import List

class Blockchain:
    def __init__(self):
        self.__chain: List[Block] = [self.__create_genesis_block()]
        self.__difficulty: int = 5
        self.__pending_transaction: List[Transaction] = []
        self.__reward = 10

    def __create_genesis_block(self) -> Block:
        genesis_block = Block(str(datetime.datetime.now()), [], "I am the Genesis Block")
        return genesis_block

    def __get_last_block(self) -> Block:
        return self.__chain[len(self.__chain) - 1]

    def mine_pending_trans(self, miner_reward_address):
        # in reality not all of the pending transaction go into the block the miner gets to pick which one to mine
        new_block = Block(str(datetime.datetime.now()), self.__pending_transaction)

        for trans in new_block.get_transactions():
            if not trans.veriry():
                new_block.remove_transaction(trans)

        new_block.mine_blocks(self.__difficulty)
        new_block.set_previous_block(self.__get_last_block().get_hash())

        print("Previous Block's Hash: " + new_block.get_previous_block())
        test_block = []
        for trans in new_block.get_transactions():
            temp = json.dumps(trans.__dict__())
            test_block.append(temp)
        print(test_block)

        self.__chain.append(new_block)
        print("Block's Hash: " + new_block.get_hash())
        print("Block added")

        reward_trans = Transaction("System", miner_reward_address, self.__reward)
        self.__pending_transaction.append(reward_trans)
        self.__pending_transaction = []

    def is_chain_valid(self) -> str:
        for x in range(1, len(self.__chain)):
            current_block = self.__chain[x]
            previous_block = self.__chain[x - 1]

            print('{} / {} => {}'.format(current_block.get_previous_block(), previous_block.get_hash(),
                                         current_block.get_previous_block() != previous_block.get_hash()))
            if current_block.get_previous_block() != previous_block.get_hash():
                return "The Chain is not valid!"
        return "The Chain is valid and secure"

    def create_transaction(self, transaction: Transaction):
        self.__pending_transaction.append(transaction)

    def get_balance(self, wallet_address) -> int:
        balance = 0
        for block in self.__chain:
            if block.get_previous_block() == "":
                # dont check the first block
                continue
            for transaction in block.get_transactions():
                if transaction.get_from_wallet() == wallet_address:
                    balance -= transaction.get_amount()
                if transaction.get_to_wallet() == wallet_address:
                    balance += transaction.get_amount()
        return balance
