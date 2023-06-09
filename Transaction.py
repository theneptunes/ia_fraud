class Transaction:
    is_fraud = 0
    values = []

    def __init__(self, amount, use_chip, mcc, has_chip, merchant_latitude, merchant_longitude, month, day_week, day, hour, distance_merchant, latitude, longitude, age):
        self.values.append(amount)
        self.values.append(use_chip)
        self.values.append(mcc)
        self.values.append(has_chip)
        self.values.append(merchant_latitude)
        self.values.append(merchant_longitude)
        self.values.append(month)
        self.values.append(day_week)
        self.values.append(day)
        self.values.append(hour)
        self.values.append(distance_merchant)
        self.values.append(latitude)
        self.values.append(longitude)
        self.values.append(age)

    def setIsFraud(self, value):
        self.is_fraud = value

    def get(self):
        return self