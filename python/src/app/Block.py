import hashlib


class Block:
    def __init__(self, timeStamp, trans, previousBlock=''):
        self.timeStamp = timeStamp
        self.trans = trans
        self.previousBlock = previousBlock
        self.difficultyIncrement = 0
        self.hash = self.calculateHash(trans, timeStamp, self.difficultyIncrement)

    def calculateHash(self, data, timeStamp, difficultyIncrement):
        data = str(str(data) + str(timeStamp) + str(difficultyIncrement)).encode()
        hash = hashlib.sha256(data)
        return hash.hexdigest()

    def mineBlock(self, difficulty):
        difficultyCheck = "9" * difficulty
        while self.hash[:difficulty] != difficultyCheck:
            self.hash = self.calculateHash(self.trans, self.timeStamp, self.difficultyIncrement)
            self.difficultyIncrement = self.difficultyIncrement + 1
