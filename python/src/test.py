from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt



# eth_k = generate_eth_key()
# prvhex = eth_k.to_hex()
# pubhex = eth_k.public_key.to_hex()
# print(prvhex)
# print('public :' + pubhex)
# data = b'this is a test'
# print(encrypt(pubhex, data))
#
# difficulty = 5
# hash = '0000x297ff3f325dbbd412f8392f1b7f868edad9d2fde5d2d74f5f230565d2640f9e9300ea246b604b8bd64d56aada4cc02f92d746be1c5291b3953530b101e6f9340'
# print(hash[:difficulty] != '0' * difficulty)
#
#
# def mine_block(self, difficulty):
#     while self.__hash[:difficulty] != '0' * difficulty:
#         self.__nonce += 1
#         self.__hash = self.calculate_hash()
#     print('Block mined:' + self.hash)
