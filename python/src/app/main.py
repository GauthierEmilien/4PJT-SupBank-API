from Transaction import Transaction
from Blockchain import Blockchain
from Cryptodome.PublicKey import RSA

# blockchain creation
xatome_money = Blockchain()

eric_key = RSA.generate(1024)
alex_key = RSA.generate(1024)
raymond_key = RSA.generate(1024)
gloria_key = RSA.generate(1024)


transaction_1 = Transaction(eric_key.publickey().export_key('DER'), alex_key.publickey().export_key('DER'), 20)
transaction_1.sign(eric_key)
xatome_money.create_transaction(transaction_1)

transaction_2 = Transaction(eric_key.publickey().export_key('DER'), raymond_key.publickey().export_key('DER'), 5)
transaction_2.sign(eric_key)
xatome_money.create_transaction(transaction_2)

transaction_3 = Transaction(alex_key.publickey().export_key('DER'), raymond_key.publickey().export_key('DER'), 10)
transaction_3.sign(alex_key)
xatome_money.create_transaction(transaction_3)

print("Gloria started minning")
xatome_money.mine_pending_trans(gloria_key.publickey().export_key('DER'))


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
print("Gloria has " + str(xatome_money.get_balance(gloria_key.publickey().export_key('DER'))) + " XatomeCoin(s) on her account")
print("Alex has " + str(xatome_money.get_balance(alex_key.publickey().export_key('DER'))) + " XatomeCoin(s) on her account")
print(xatome_money.is_chain_valid())
