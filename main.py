import lr
import lgbm
import isolation_forest
import random_forest
import gnb
import Transaction
## Year,Month,Day,Time,Amount,Use Chip,Merchant Name,Merchant City,Is Fraud?
     
# Use chip
# Swipe Transaction 0
# Online Transaction 1

# Merchant City
# La Verne 0
# Monterey Park 1
# Mira Loma 2

t = Transaction.Transaction(
    2020,
    12,
    4,
    1684701282.0, #21/05/2023
    2000.0,
    0,
    -727612092139916043,
    1
)
predicted = lr([t.values])
print(predicted)
print(gnb([t.values]))
if predicted[0] == 0:
    print("OK")
else:
    print("FRAUDE")

print("LGBM")
predicted = lgbm([t.values])
print(predicted)
print(gnb([t.values]))
if predicted[0] == 0:
    print("OK")
else:
    print("FRAUDE")

print("RF")
predicted = random_forest([t.values])
print(predicted)
print(gnb([t.values]))
if predicted[0] == 0:
    print("OK")
else:
    print("FRAUDE")

print("IF")
predicted = isolation_forest([t.values])
print(predicted)
print(gnb([t.values]))
if predicted[0] == 0:
    print("OK")
else:
    print("FRAUDE")