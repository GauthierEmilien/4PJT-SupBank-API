from threading import Thread, Event
from Blockchain import Blockchain
from Block import Block
import datetime
import json


class Mining(Thread):

    def __init__(self, blockchain: Blockchain, reward_address: bytes):
        Thread.__init__(self)
        self.__blockchain = blockchain
        self.__reward_address = reward_address
        self.__stop = False

    def run(self) -> None:
        new_block = Block(str(datetime.datetime.now()), self.__blockchain.get_pending_transaction())

        for trans in new_block.get_transactions():
            if not trans.verify():
                new_block.remove_transaction(trans)

        if len(new_block.get_transactions()) < 1:
            print('No valid transaction to add in block')
            return

        self.__mine_block(new_block)
        new_block.set_previous_block(self.__blockchain.get_last_block().get_hash())

        print("Previous Block's Hash: " + new_block.get_previous_block())
        test_block = []
        for trans in new_block.get_transactions():
            temp = json.dumps(trans.__dict__())
            test_block.append(temp)
        print(test_block)

        if not self.__stop:
            from global_var import server
            server.send_block(new_block.__dict__())

    def stop(self):
        print('stop thread')
        self.__stop = True


    def __mine_block(self, block: Block):
        difficulty = self.__blockchain.get_difficulty()
        difficulty_check = '0' * difficulty
        while not self.__stop and block.get_hash()[:difficulty] != difficulty_check:
            block.calculate_hash()
            block.update_nonce()
