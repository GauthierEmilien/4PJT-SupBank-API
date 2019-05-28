from Transaction import Transaction
from Block import Block
from typing import List
from threading import Lock
from database import DB

lock = Lock()


class Blockchain:  # Add Thread inheritance for multithreading
    DB = DB('xatomeDB')

    def __init__(self):
        self.__chain: List[Block] = []
        self.__difficulty: int = 5
        self.__pending_transaction: List[Transaction] = []
        self.__reward = 10

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
    def add_block(cls, block: dict):  # Add a block to blockchain database
        from global_var import block_collection
        cls.DB.insert(block_collection, block)

    """ /!\/!\ DO NOT CALL ANYMORE !!! /!\/!\ """

    # def create_genesis_block(self) -> Block:  # create the first block of the blockchain (to call only once)
    #     genesis_block = Block(str(datetime.datetime.now()), [], "I am the Genesis Block")
    #     return genesis_block

    """ /!\/!\ DO NOT CALL ANYMORE !!! /!\/!\ """

    def get_last_block(self) -> Block:  # return the last block of the blockchain
        return self.__chain[-1]

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

    def get_difficulty(self) -> int:
        return self.__difficulty
