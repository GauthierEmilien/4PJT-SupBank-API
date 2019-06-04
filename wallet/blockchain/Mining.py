from threading import Thread, Lock
import datetime
import json

from blockchain.Blockchain import Blockchain
from blockchain.Block import Block
from server.Client import Client

lock = Lock()


class Mining(Thread):

    def __init__(self, blockchain: Blockchain, reward_address: bytes, host: str):
        Thread.__init__(self)
        self.__blockchain = blockchain
        self.__host = host
        self.__reward_address = reward_address
        self.__stop = False
        transactions = []
        for t in self.__blockchain.get_pending_transaction():
            transactions.append(t)
        self.__new_block = Block(str(datetime.datetime.now()), transactions)
        self.start()

    def run(self) -> None:
        print('start mining')
        for trans in self.__new_block.get_transactions():
            if not trans.verify():
                self.__new_block.remove_transaction(trans)

        if len(self.__new_block.get_transactions()) < 1:
            print('No valid transaction to add in block')
            return

        self.__mine_block(self.__new_block)
        self.__new_block.set_previous_block(self.__blockchain.get_last_block().get_hash())

        print("Previous Block's Hash: " + self.__new_block.get_previous_block())
        test_block = []
        for trans in self.__new_block.get_transactions():
            temp = json.dumps(trans.__dict__())
            test_block.append(temp)
        print(test_block)

        if not self.__stop:
            self.__send_block()
        print('thread finished')

    def stop(self):
        print('stop thread')
        self.__stop = True

    def __mine_block(self, block: Block):
        difficulty = self.__blockchain.get_difficulty()
        difficulty_check = '0' * difficulty
        while not self.__stop and block.get_hash()[:difficulty] != difficulty_check:
            block.calculate_hash()
            block.update_nonce()

    def __send_block(self):
        print('send block')
        block = self.__new_block.__dict__()
        Client.send_to_every_nodes(self.__host, 'block', block, False, wait=True)
        print('block sent')

        is_block_accepted = True

        # lock.acquire()
        # for is_valid in Client.block_is_valid:
        #     if is_valid == 'false':
        #         print('block not accepted')
        #         is_block_accepted = False
        # lock.release()

        while not Client.block_is_valid_queue.empty():
            if Client.block_is_valid_queue.get() == 'false':
                print('block not accepted')
                is_block_accepted = False
                Client.block_is_valid_queue.task_done()

        if not is_block_accepted:
            Client.send_to_every_nodes(self.__host, 'block_accepted', 'false')
        else:
            self.__blockchain.clear_pending_transaction([t.__dict__() for t in self.__new_block.get_transactions()])

            print('block sended =>', block)
            Client.send_to_every_nodes(self.__host, 'block_accepted', block, wait=True)
            self.__blockchain.add_block(block)
            self.__blockchain.get_update()
            print('accepted block')

    def get_reward_address(self) -> bytes:
        return self.__reward_address
