import base64
import datetime
from hashlib import sha256

from ecdsa import SigningKey, VerifyingKey


class Transaction:

    def __init__(self, from_address: VerifyingKey, to_address: str, amount: float):
        self.__from_address: VerifyingKey = from_address
        self.__to_address: str = to_address
        self.__amount: float = amount
        self.__timestamp = datetime.datetime.now()
        self.__signature = None

    """
    Creates a SHA256 hash of the transaction
    """

    def calculateHash(self) -> str:
        return str(sha256(str(self.__from_address.to_string().hex() + self.__to_address + str(self.__amount) + str(
            self.__timestamp)).encode()))

    """
    Signs a transaction with the given signingKey (which is an Elliptic keypair
    object that contains a private key). The signature is then stored inside the
    transaction object and later stored on the blockchain.
    """

    def signTransaction(self, signing_key: SigningKey):
        pub_key = signing_key.get_verifying_key()
        if pub_key.to_string().hex() != self.__from_address.to_string().hex():
            raise Exception('You cannot sign transactions for other wallets!')

        hash_tx = self.calculateHash()
        sig = signing_key.sign(hash_tx.encode())
        self.__signature = sig.hex()

    """
    Checks if the signature is valid (transaction has not been tampered with).
    It uses the fromAddress as the public key.
    """

    def is_valid(self) -> bool:
        if self.__from_address is None:
            return True

        if not self.__signature or len(self.__signature) == 0:
            raise Exception('No signature in self transaction')

        # try:
        return self.__from_address.verify(self.__signature, base64.b64encode(self.calculateHash().encode()))
        # except BadSignatureError:
        #     print(BadSignatureError)
        #     return False

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
