from Transaction import Transaction
from Blockchain import Blockchain

# blockchain creation
xatome_money = Blockchain()

xatome_money.create_transaction(Transaction("Erick", "Alex", 3.2))
xatome_money.create_transaction(Transaction("Erick", "Raymond", 1))
xatome_money.create_transaction(Transaction("Alex", "Raymond", 5.12))

print("Gloria started minning")

xatome_money.mine_pending_trans("Gloria")
xatome_money.create_transaction(Transaction("Zining", "Alex", 0.01))
xatome_money.create_transaction(Transaction("Klay", "Erick", 100))
xatome_money.create_transaction(Transaction("Raymond", "Erick", 0.0000001))

print("Gloria started minning")
xatome_money.mine_pending_trans("Gloria")

print("Gloria has " + str(xatome_money.get_balance("Gloria")) + " XatomeCoin(s) on her account")
print("Gloria has " + str(xatome_money.get_balance("Alex")) + " XatomeCoin(s) on her account")
print(xatome_money.is_chain_valid())
