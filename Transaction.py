class Transaction:
    # Year,Month,Day,Time,Amount,Use Chip,Merchant Name,Merchant City,Is Fraud?
    is_fraud = 0
    values = []

    def __init__(self, year, month, day, time, amount, use_chip, merchant_name, merchant_city):
        self.values.append(year)
        self.values.append(month)
        self.values.append(day)
        self.values.append(time)
        self.values.append(amount)
        self.values.append(use_chip)
        self.values.append(merchant_name)
        self.values.append(merchant_city)

    def setIsFraud(self, value):
        self.is_fraud = value

    def get(self):
        return self