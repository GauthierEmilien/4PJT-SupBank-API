import datetime
from hashlib import sha256
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt


class Transaction:

    def __init__(self, from_address: str, to_address: str, amount: int):
        self.__from_address: str = from_address
        self.__to_address: str = to_address
        self.__amount: int = amount
        self.__timestamp = datetime.datetime.now()
        self.__signature = None


    """
    Creates a SHA256 hash of the transaction
    """
    def calculateHash(self) -> str:
        return str(sha256(self.__from_address + self.__to_address + self.__amount + self.__timestamp))


    """
    Signs a transaction with the given signingKey (which is an Elliptic keypair
    object that contains a private key). The signature is then stored inside the
    transaction object and later stored on the blockchain.
    """
    def signTransaction(self, signingKey: str):
        if signingKey.getPublic('hex') != self.__from_address:
            raise Exception('You cannot sign transactions for other wallets!')

        hash_tx = self.calculateHash()
        sig = signingKey.sign(hash_tx, 'base64')

        self.__signature = sig.toDER('hex')


    """
    Checks if the signature is valid (transaction has not been tampered with).
    It uses the fromAddress as the public key.
    """
    def is_valid(self) -> bool:
        if self.__from_address is None:
            return True

        if not self.__signature or self.__signature.length == 0:
            raise Exception('No signature in self transaction')

        # TODO : faire fonctionner la ligne
        publicKey = generate_key(self.__from_address, 'hex')
        return publicKey.verify(self.calculateHash(), self.__signature)


    def get_from_address(self):
        return self.__from_address


    def get_to_address(self):
        return self.__to_address


    def get_amount(self):
        return self.__amount


print('0' * 4)
