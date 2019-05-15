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

# import socketio
#
# # create a Socket.IO server
# sioserv = socketio.Server()
#
# # wrap with a WSGI application
# app = socketio.WSGIApp(sioserv)
#
#
# @sioserv.on('connect')
# def connect(sid, environ):
#     print('connect ', sid)
#
#
# @sioserv.on('disconnect')
# def disconnect(sid):
#     print('disconnect ', sid)
#
#
# sio = socketio.Client()
# sio.connect('http://localhost:8080')
#
#
# @sio.on('connect')
# def on_connect():
#     print('I\'m connected!')
#
#
# @sio.on('message')
# def on_message(data):
#     print('I received a message!')
#
#
# @sio.on('my message')
# def on_message(data):
#     print('I received a custom message!')
#
#
# @sio.on('disconnect')
# def on_disconnect():
#     print('I\'m disconnected!')
#
#
# sio.emit('my message', {'foo': 'bar'})

# from ecdsa import SigningKey, SECP256k1
#
# from python.src.Blockchain import Blockchain
# from python.src.Transaction import Transaction
#
# priv_key = SigningKey.generate(curve=SECP256k1) # uses SECP256k1
# pub_key = priv_key.get_verifying_key()
# print('public \n')
# print(pub_key.to_string().hex() + '\n')
# print('private \n')
# print(priv_key.to_string().hex())
#
#
# # From that we can calculate your public key (which doubles as your wallet address)
# my_wallet_address = pub_key
# xatomeCoin = Blockchain()
#
# # Create a transaction & sign it with your key
# tx1 = Transaction(my_wallet_address, 'address1', 50)
# tx1.signTransaction(priv_key)
# print(tx1)
# xatomeCoin.add_transaction(tx1)
#
# # Mine pending Transaction
# xatomeCoin.mine_pending_transaction(my_wallet_address)
#
# # Create a second transaction & sign it with your key
# tx2 = Transaction(my_wallet_address, 'address2', 250)
# tx2.signTransaction(priv_key)
# print(tx2)
# xatomeCoin.add_transaction(tx2)
#
# # Mine pending Transaction
# xatomeCoin.mine_pending_transaction(my_wallet_address)
#
# print()
# print("Balance of xavier is : " + str(xatomeCoin.get_balance_of_address(my_wallet_address)))
# from Crypto.PublicKey import RSA, ECC
#
#
# private_key = RSA.generate(1024)
# public_key = private_key.publickey()
# print(private_key.exportKey)
# print(public_key.export_key().decode())
#
# private = ECC.generate(curve='secp256r1')
#
# print(private)
# print(private.export_key(format='Base64'))

# from Crypto.PublicKey import ECC
# from Utils import getKeyFromECC
#
# key = ECC.generate(curve="secp256r1")
#
#
#
# print(key.export_key(format='PEM'))
# print(getKeyFromECC(key.export_key(format='PEM')))
# print(getKeyFromECC(key.public_key().export_key(format='PEM')))

from Crypto.PublicKey import ECC
from Utils import getPubKeyFromECC, getPrivKeyFromECC
from Blockchain import Blockchain
from Transaction import Transaction

key_pair = ECC.generate(curve="secp256r1")
pub_key = getPubKeyFromECC(key_pair.public_key().export_key(format='PEM'))
priv_key = getPrivKeyFromECC(key_pair.export_key(format='PEM'))

# From that we can calculate your public key (which doubles as your wallet address)
my_wallet_address = pub_key
xatomeCoin = Blockchain()

# Create a transaction & sign it with your key
tx1 = Transaction(my_wallet_address, 'address1', 50)
tx1.signTransaction(key_pair)
print(tx1)
xatomeCoin.add_transaction(tx1)

# Mine pending Transaction
xatomeCoin.mine_pending_transaction(my_wallet_address)

# Create a second transaction & sign it with your key
tx2 = Transaction(my_wallet_address, 'address2', 250)
tx2.signTransaction(key_pair)
print(tx2)
xatomeCoin.add_transaction(tx2)

# Mine pending Transaction
xatomeCoin.mine_pending_transaction(my_wallet_address)

print()
print("Balance of xavier is : " + str(xatomeCoin.get_balance_of_address(my_wallet_address)))
from Crypto.PublicKey import RSA, ECC


private_key = RSA.generate(1024)
public_key = private_key.publickey()
print(private_key.exportKey)
print(public_key.export_key().decode())

private = ECC.generate(curve='secp256r1')

print(private)
print(private.export_key(format='Base64'))