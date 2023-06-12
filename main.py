import rf
import Transaction
## Amount,Use Chip,MCC,Has Chip,Merchant Latitude,Merchant Longitude,Month,Day of Week,Day,Hour,Distance to Merchant,Latitude,Longitude,Age,Is Fraud
     
# Use Chip
# 0 - Chip Transaction
# 1 - Online Transaction
# 2 - Swipe Transaction

# Has Chip
# 0 - No
# 1 - Yes

# Day of Week
# 0 - Segunda
# ...
# 6 - Domingo

t = Transaction.Transaction(
    1200,
    0.0,
    5712.0,
    1.0,
    37.42488662030914,
    -91.83121755030102,
    4.0,
    4.0,
    5.0,
    19.0,
    350.5380032727895, # 10
    35.58,
    -88.5,
    26.0
)

predicted = rf([t.values])
#print(predicted)
#print(gnb([t.values]))
if predicted[0] == 0:
    print("OK")
else:
    print("FRAUDE")