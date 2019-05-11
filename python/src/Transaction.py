import datetime
from hashlib import sha256

from fastecdsa import curve, ecdsa


class Transaction:

    def __init__(self, from_address: str, to_address: str, amount: float):
        self.__from_address: str = from_address
        self.__to_address: str = to_address
        self.__amount: float = amount
        self.__timestamp = datetime.datetime.now()
        self.__signature = None

    """
    Creates a SHA256 hash of the transaction
    """

    def calculateHash(self) -> str:
        return str(sha256(self.__from_address + self.__to_address + str(self.__amount) + str(self.__timestamp)))

    """
    Signs a transaction with the given signingKey (which is an Elliptic keypair
    object that contains a private key). The signature is then stored inside the
    transaction object and later stored on the blockchain.
    """

    def signTransaction(self, signing_pub_key: str, signing_priv_key: str):
        if signing_pub_key != self.__from_address:
            raise Exception('You cannot sign transactions for other wallets!')

        hash_tx = self.calculateHash()
        r, s = ecdsa.sign(hash_tx, signing_priv_key, curve.secp256k1, sha256)
        self.__signature = (r, s)

    """
    Checks if the signature is valid (transaction has not been tampered with).
    It uses the fromAddress as the public key.
    """

    def is_valid(self) -> bool:
        if self.__from_address is None:
            return True

        if not self.__signature or self.__signature.length == 0:
            raise Exception('No signature in self transaction')

        return ecdsa.verify(self.__signature, self.calculateHash(), self.__from_address, curve.secp256k1, sha256)

    def get_from_address(self):
        return self.__from_address

    def get_to_address(self):
        return self.__to_address

    def get_amount(self):
        return self.__amount
