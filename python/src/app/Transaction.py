from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA

class Transaction:
    def __init__(self, from_wallet, to_wallet, amount):
        self.__from_wallet = from_wallet
        self.__to_wallet = to_wallet
        self.__amount = amount
        self.__hash = None
        self.__signature = None

    def get_from_wallet(self):
        return self.__from_wallet

    def get_to_wallet(self):
        return self.__to_wallet

    def get_amount(self):
        return self.__amount

    def sign(self, private_key: RSA.RsaKey):
        self.__hash = SHA256.new(self.__str__().encode())
        self.__signature = pkcs1_15.new(private_key).sign(self.__hash)

    def veriry(self) -> bool:
        try:
            pub_key = RSA.import_key(self.__from_wallet)
            pkcs1_15.new(pub_key).verify(self.__hash, self.__signature)
            return True
        except (ValueError, TypeError):
            return False

    def __str__(self):
        print('{}'.format(self.__from_wallet, self.__to_wallet, self.__amount))
        return '{}'.format(self.__from_wallet, self.__to_wallet, self.__amount)