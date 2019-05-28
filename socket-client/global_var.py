from Cryptodome.PublicKey import RSA
import Blockchain
import Server

block_collection = 'blocks'

server = Server.Server()

eric_key = RSA.generate(1024)
alex_key = RSA.generate(1024)
my_key = RSA.generate(1024)

xatome_money = Blockchain.Blockchain()
xatome_money.get_update()