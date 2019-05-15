import datetime
from hashlib import sha256

from Crypto.PublicKey.ECC import EccKey
from Crypto.Signature import DSS

from Utils import getPubKeyFromECC


class Transaction:

    def __init__(self, from_address: str, to_address: str, amount: float):
        self.__from_address: str = from_address
        self.__to_address: str = to_address
        self.__amount: float = amount
        self.__timestamp = datetime.datetime.now()
        self.__signature = None
        self.__signKey = None

    """
    Creates a SHA256 hash of the transaction
    """

    def calculateHash(self) -> sha256:
        return sha256(str(
            self.__from_address + self.__to_address + str(self.__amount) + str(self.__timestamp.timestamp())).encode())

    """
    Signs a transaction with the given signingKey (which is an Elliptic keypair
    object that contains a private key). The signature is then stored inside the
    transaction object and later stored on the blockchain.
    """

    def signTransaction(self, signing_key: EccKey):
        pub_key = getPubKeyFromECC(signing_key.public_key().export_key(format='PEM'))
        if pub_key != self.__from_address:
            raise Exception('You cannot sign transactions for other wallets!')

        hash_tx = self.calculateHash()

        # sig = signing_key.sign(hash_tx.encode())
        # self.__signature = sig.hex()
        self.__signKey = DSS.new(signing_key, 'fips-186-3')
        self.__signature = self.__signKey.sign(hash_tx)

    """
    Checks if the signature is valid (transaction has not been tampered with).
    It uses the fromAddress as the public key.
    """

    def is_valid(self) -> bool:
        if self.__from_address is None:
            return True

        if not self.__signature or len(self.__signature) == 0:
            raise Exception('No signature in self transaction')

        return DSS.new(self.__signKey, 'fips-186-3').verify(self.calculateHash().encode(), self.__signature)

    def get_from_address(self):
        return self.__from_address

    def get_to_address(self):
        return self.__to_address

    def get_amount(self):
        return self.__amount

    # def _default(self, obj):
    #     return getattr(obj.__class__, "to_json", self._default.default)(obj)
    # def to_json(self):  # New special method.
    #     """ Convert to JSON format string representation. """
    #     return '{"name": "%s"}' % self.get_amount()
