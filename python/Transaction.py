import datetime
import hashlib
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt


class Transaction:

    def __init__(self, from_address, to_address, amount):
        self.__from_address = from_address
        self.to_address = to_address
        self.__amount = amount
        self.__timestamp = datetime.datetime.now()
        self.__signature = None

    def calculateHash(self):
        return hashlib.sha256(self.__from_address + self.to_address + self.__amount + self.__timestamp).toString()

    def signTransaction(self, signingKey):
        if signingKey.getPublic('hex') != self.__from_address:
            raise Exception('You cannot sign transactions for other wallets!')

        hash_tx = self.calculateHash()
        sig = signingKey.sign(hash_tx, 'base64')

        self.__signature = sig.toDER('hex')

    def isValid(self):
        if self.__from_address is None:
            return True

        if not self.__signature or self.__signature.length == 0:
            raise Exception('No signature in self transaction')

        # TODO : faire fonctionner la ligne
        publicKey = generate_key(self.__from_address, 'hex')
        return publicKey.verify(self.calculateHash(), self.__signature)


print('0' * 4)
