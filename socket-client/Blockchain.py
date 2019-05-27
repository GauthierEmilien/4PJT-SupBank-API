import datetime
import json
from Transaction import Transaction
from Block import Block
from typing import List
from threading import Thread, Lock
from database import DB

lock = Lock()


class Blockchain:  # Add Thread inheritance for multithreading
    DB = DB('xatomeDB')

    def __init__(self):
        self.__chain: List[Block] = []
        self.__difficulty: int = 5
        self.__pending_transaction: List[Transaction] = []
        self.__reward = 10

    def start(self, miner_reward_address: bytes):
        t = Thread(target=self.__mine_pending_trans, args=(miner_reward_address,))
        t.start()

    def get_update(self):  # Get the last version of the blockchain from database
        from global_var import block_collection
        block_cursor = Blockchain.DB.get_all(block_collection)
        self.__chain = []
        for block in block_cursor:
            self.__chain.append(Block.from_dict(block))
        print(self.__chain)

    @classmethod
    def update_all(cls, blocks: List[dict]):
        from global_var import block_collection
        cls.DB.delete_all(block_collection)
        cls.DB.insert_many(block_collection, blocks)

    @classmethod
    def add_block(cls, block: Block):  # Add a block to blockchain database
        from global_var import block_collection
        cls.DB.insert(block_collection, block.__dict__())

    """ /!\/!\ DO NOT CALL ANYMORE !!! /!\/!\ """

    # def create_genesis_block(self) -> Block:  # create the first block of the blockchain (to call only once)
    #     genesis_block = Block(str(datetime.datetime.now()), [], "I am the Genesis Block")
    #     return genesis_block

    """ /!\/!\ DO NOT CALL ANYMORE !!! /!\/!\ """

    def __get_last_block(self) -> Block:  # return the last block of the blockchain
        return self.__chain[-1]

    def __mine_pending_trans(self, miner_reward_address: bytes):  # maybe the thread start() methode
        # in reality not all of the pending transaction go into the block the miner gets to pick which one to mine
        new_block = Block(str(datetime.datetime.now()), self.__pending_transaction)

        for trans in new_block.get_transactions():
            if not trans.verify():
                new_block.remove_transaction(trans)

        if len(new_block.get_transactions()) < 1:
            print('No valid transaction to add in block')
            return

        new_block.calculate_hash()
        new_block.mine_blocks(self.__difficulty)
        new_block.set_previous_block(self.__get_last_block().get_hash())

        # USELESS : print block informations after mining
        print("Previous Block's Hash: " + new_block.get_previous_block())
        test_block = []
        for trans in new_block.get_transactions():
            temp = json.dumps(trans.__dict__())
            test_block.append(temp)
        print(test_block)

        from global_var import block_collection
        Blockchain.DB.insert(block_collection, new_block.__dict__())
        self.get_update()

        print("Block's Hash: " + new_block.get_hash())
        print("Block added")

        from global_var import server
        server.send_block(new_block.__dict__())

        # reward_trans = Transaction(b"System", miner_reward_address, self.__reward)
        # self.__pending_transaction.append(reward_trans)
        self.__pending_transaction = []

    def is_chain_valid(self, block: Block = None) -> bool:  # verify if blockchain is valid
        if block:
            self.__chain.append(block)

        for x in range(1, len(self.__chain)):
            current_block = self.__chain[x]
            previous_block = self.__chain[x - 1]
            if current_block.get_previous_block() != previous_block.get_hash():
                self.__chain.pop()
                return False
        return True

    def add_transaction(self, transaction: Transaction):  # add a transaction to pending transactions list
        self.__pending_transaction.append(transaction)

    def get_balance(self, wallet_address: bytes) -> int:
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

    def get_pending_transaction(self) -> List[Transaction]:
        return self.__pending_transaction

    def get_blocks(self) -> List[Block]:
        return self.__chain
