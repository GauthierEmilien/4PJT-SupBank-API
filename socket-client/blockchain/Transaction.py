from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA


class Transaction:
    def __init__(self, timestamp: str, from_wallet: bytes, to_wallet: bytes, amount: int, signature: bytes = b''):
        self.__from_wallet = from_wallet
        self.__to_wallet = to_wallet
        self.__amount = amount
        self.__signature = signature
        self.__timestamp = timestamp

    @classmethod
    def from_dict(cls, transaction: dict):
        return Transaction(transaction.get('timestamp'),
                           bytes.fromhex(transaction.get('from_wallet')),
                           bytes.fromhex(transaction.get('to_wallet')),
                           transaction.get('amount'),
                           bytes.fromhex(transaction.get('signature')))

    def get_from_wallet(self) -> bytes:
        return self.__from_wallet

    def get_to_wallet(self) -> bytes:
        return self.__to_wallet

    def get_amount(self) -> int:
        return self.__amount

    def get_signature(self) -> bytes:
        return self.__signature

    def sign(self, private_key: RSA.RsaKey):
        hash = SHA256.new(self.__str__().encode())
        self.__signature = pkcs1_15.new(private_key).sign(hash)

    def verify(self) -> bool:
        try:
            hash = SHA256.new(self.__str__().encode())
            pub_key = RSA.import_key(self.__from_wallet)
            pkcs1_15.new(pub_key).verify(hash, self.__signature)
            print('signature is ok')
            return True
        except (ValueError, TypeError) as e:
            print('signature is not ok :', e)
            return False

    def __str__(self) -> str:
        return '{}'.format(self.__from_wallet, self.__to_wallet, self.__amount, self.__timestamp)

    def __dict__(self) -> dict:
        return {
            'from_wallet': self.__from_wallet.hex(),
            'to_wallet': self.__to_wallet.hex(),
            'amount': self.__amount,
            'signature': self.__signature.hex(),
            'timestamp': self.__timestamp
        }

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__signature == other.__signature
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
