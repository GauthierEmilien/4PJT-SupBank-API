from Transaction import Transaction
from Blockchain import Blockchain
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.Random import get_random_bytes
import sys

# blockchain creation
xatome_money = Blockchain()

eric_key = RSA.generate(1024)
alex_key = RSA.generate(1024)
gloria_key = RSA.generate(1024)


transaction_1 = Transaction(eric_key.publickey().export_key('DER'), alex_key.publickey().export_key('DER'), 10)
transaction_1.sign(alex_key)
print('signature is', transaction_1.veriry())
# xatome_money.create_transaction(transaction_1)
# xatome_money.create_transaction(Transaction("Erick", "Raymond", 5))
# xatome_money.create_transaction(Transaction("Alex", "Raymond", 10))
#
# print("Gloria started minning")
# xatome_money.mine_pending_trans("Gloria")
#
# xatome_money.create_transaction(Transaction("Zining", "Alex", 5))
# xatome_money.create_transaction(Transaction("Klay", "Erick", 20))
# xatome_money.create_transaction(Transaction("Raymond", "Erick", 5))
#
# print("Gloria started minning")
# xatome_money.mine_pending_trans("Gloria")
#
# xatome_money.create_transaction(Transaction("Zining", "Alex", 5))
# xatome_money.create_transaction(Transaction("Klay", "Erick", 20))
# xatome_money.create_transaction(Transaction("Raymond", "Erick", 5))
#
# print("Gloria started minning")
# xatome_money.mine_pending_trans("Gloria")
#
# print("Gloria has " + str(xatome_money.get_balance("Gloria")) + " XatomeCoin(s) on her account")
# print("Alex has " + str(xatome_money.get_balance("Alex")) + " XatomeCoin(s) on her account")
# print(xatome_money.is_chain_valid())
