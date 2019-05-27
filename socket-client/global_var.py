from Cryptodome.PublicKey import RSA
from Blockchain import Blockchain

eric_key = RSA.generate(1024)
alex_key = RSA.generate(1024)
my_key = RSA.generate(1024)

xatome_money = Blockchain()