from Transaction import Transaction
from Blockchain import Blockchain
#
ezmoney = Blockchain()
ezmoney.createTrans(Transaction("Erick", "Alex", 3.2))
ezmoney.createTrans(Transaction("Erick", "Raymond", 1))
ezmoney.createTrans(Transaction("Alex", "Raymond", 5.12))

print("Gloria started minning")

ezmoney.minePendingTrans("Gloria")
ezmoney.createTrans(Transaction("Zining", "Alex", 0.01))
ezmoney.createTrans(Transaction("Klay", "Erick", 100))
ezmoney.createTrans(Transaction("Raymond", "Erick", 0.0000001))

print("Gloria started minning")
ezmoney.minePendingTrans("Gloria")

print("Gloria has " + str(ezmoney.getBalance("Gloria")) + " EZCoins on her account")
print("Gloria has " + str(ezmoney.getBalance("Alex")) + " EZCoins on her account")
print(ezmoney.isChainValid())

print('coucou')