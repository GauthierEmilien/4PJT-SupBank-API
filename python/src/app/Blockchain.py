import datetime
import json
import pprint

from Block import Block
from Transaction import Transaction


class Blockchain:
    def __init__(self):
        self.chain = [self.GenesisBlock()]
        self.difficulty = 5
        self.pendingTransaction = []
        self.reward = 10

    def GenesisBlock(self):
        genesisBlock = Block(str(datetime.datetime.now()), "I am the Gensis Block")
        return genesisBlock

    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    def minePendingTrans(self, minerRewardAddress):
        # in reality not all of the pending transaction go into the block the miner gets to pick which one to mine
        newBlock = Block(str(datetime.datetime.now()), self.pendingTransaction)
        newBlock.mineBlock(self.difficulty)
        newBlock.previousBlock = self.getLastBlock().hash

        print("Previous Block's Hash: " + newBlock.previousBlock)
        testChain = []
        for trans in newBlock.trans:
            temp = json.dumps(trans.__dict__, indent=5, separators=(',', ': '))
            testChain.append(temp)
        pprint.pprint(testChain)

        self.chain.append(newBlock)
        print("Block's Hash: " + newBlock.hash)
        print("Block added")

        rewardTrans = Transaction("System", minerRewardAddress, self.reward)
        self.pendingTransaction.append(rewardTrans)
        self.pendingTransaction = []

    def isChainValid(self):
        for x in range(1, len(self.chain)):
            currentBlock = self.chain[x]
            previousBlock = self.chain[x - 1]

            if (currentBlock.previousBlock != previousBlock.hash):
                return ("The Chain is not valid!")
        return ("The Chain is valid and secure")

    def createTrans(self, transaction):
        self.pendingTransaction.append(transaction)

    def getBalance(self, walletAddress):
        balance = 0
        for block in self.chain:
            if block.previousBlock == "":
                # dont check the first block
                continue
            for transaction in block.trans:
                if transaction.fromWallet == walletAddress:
                    balance -= transaction.amount
                if transaction.toWallet == walletAddress:
                    balance += transaction.amount
        return balance
