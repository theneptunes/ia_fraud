import random_forest
import logistic_progression

#User,Card,Year,Month,Day,Time,Amount,Use Chip,Merchant Name,Merchant City,Merchant State,Zip,MCC,Errors?,Is Fraud?

predicted = random_forest('Campinas-SP', 2000,'Noite','Comida')
if predicted[0] == 0:
    print("OK")
else:
    print("FRAUDE")

predicted_LG = logistic_progression('Campinas-SP', 2000,'Noite','Comida')
if predicted_LG[0] == 0:
    print("OK")
else:
    print("FRAUDE")