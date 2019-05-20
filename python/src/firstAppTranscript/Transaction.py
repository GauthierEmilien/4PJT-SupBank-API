import datetime
# from hashlib import sha256
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Hash import SHA256

from firstAppTranscript.Utils import getPubKeyFromRSA


class Transaction:

    def __init__(self, from_address: RsaKey, to_address: RsaKey, amount: float):
        self.__from_address: RsaKey = from_address
        self.__to_address: RsaKey = to_address
        self.__amount: float = amount
        self.__timestamp = datetime.datetime.now()
        self.__signature = None
        self.__signKey = None

    """
    Creates a SHA256 hash of the transaction
    """

    def calculateHash(self) -> SHA256:
        return SHA256.new(str(
            self.__from_address.export_key().decode() + self.__to_address.export_key().decode() + str(self.__amount) + str(self.__timestamp.timestamp())).encode())

    """
    Signs a transaction with the given signingKey (which is an Elliptic keypair
    object that contains a private key). The signature is then stored inside the
    transaction object and later stored on the blockchain.
    """

    def signTransaction(self, receiverPK):

        if getPubKeyFromRSA(str(receiverPK.publickey().export_key().decode())) \
                != getPubKeyFromRSA(str(self.__to_address.publickey().export_key().decode())):
            raise Exception('You cannot sign transactions for other wallets!')

        message = self.calculateHash()
        # Instantiating PKCS1_OAEP object with the public key for encryption
        self.__signature = PKCS1_OAEP.new(key=receiverPK).encrypt(message.digest())

    """
    Checks if the signature is valid (transaction has not been tampered with).
    It uses the fromAddress as the public key.
    """

    def is_valid(self) -> bool:
        if self.__from_address is None:
            return True

        if not self.__signature or len(self.__signature) == 0:
            raise Exception('No signature in self transaction')

        # # Instantiating PKCS1_OAEP object with the private key for decryption
        # decrypt = PKCS1_OAEP.new(key=self.__signKey)
        #
        # # Decrypting the message with the PKCS1_OAEP object
        # decrypted_message = decrypt.decrypt(self.calculateHash().digest())
        # print(decrypted_message)
        # if decrypted_message == self.calculateHash():
        #     return True
        # return False



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
