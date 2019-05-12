import datetime
from hashlib import sha256

from ecdsa import SigningKey, VerifyingKey, SECP256k1


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

    def signTransaction(self, signing_key: SigningKey):
        pub_key = signing_key.get_verifying_key()

        if pub_key.to_string().hex() != self.__from_address:
            raise Exception('You cannot sign transactions for other wallets!')

        hash_tx = self.calculateHash()
        r, s = signing_key.sign(hash_tx, sigencode=SECP256k1, hashfunc=sha256)
        self.__signature = (r, s)

    """
    Checks if the signature is valid (transaction has not been tampered with).
    It uses the fromAddress as the public key.
    """

    def is_valid(self) -> bool:
        if self.__from_address is None:
            return True

        if not self.__signature or len(self.__signature) == 0:
            raise Exception('No signature in self transaction')

        return ecdsa.verify(self.__signature, self.calculateHash(), self.__from_address, curves.SECP256k1, sha256)

    def get_from_address(self):
        return self.__from_address

    def get_to_address(self):
        return self.__to_address

    def get_amount(self):
        return self.__amount


sk = SigningKey.generate(curve=SECP256k1)
vk = sk.get_verifying_key()
vk_pem = vk.to_pem()
vk2 = VerifyingKey.from_pem(vk_pem)
# vk and vk2 are the same key
print(vk2)
