from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import pandas as pd 
from sklearn.metrics import classification_report
import datetime

df = pd.read_csv("./User0_credit_card_transactions.csv")

df = df.drop(['User'],axis=1)
df = df.drop(['Card'],axis=1)
df = df.drop(['Merchant State'],axis=1)
df = df.drop(['Zip'],axis=1)
df = df.drop(['MCC'],axis=1)
df = df.drop(['Errors?'],axis=1)


my_date = datetime.datetime(2023,5,5)
converted_timestamps = {}
for i in df['Time']:
    timestamp = datetime.datetime.timestamp(my_date)
    time = str(i).split(':')
    my_time = datetime.time(int(time[0]), int(time[1]))
    combined_datetime = my_date.combine(my_date, my_time)
    timestamp = datetime.datetime.timestamp(combined_datetime)
    converted_timestamps[i] = timestamp

df['Time'] = df['Time'].replace(converted_timestamps)

amounts = {}
for i in df['Amount']:
    amounts[i] = str(i).split('$')[1]
df['Amount'] = df['Amount'].replace(amounts)

#df["Use Chip"] = df["Use Chip"].replace({"Swipe Transaction": 0, "Online Transaction": 1, "Chip Transaction": 2})


for c in ['Use Chip','Merchant City']:
    values = {}
    count = 0
    for i in df[c]:
        if values.get(i) is None:
            values[i] = count
            count += 1
    df[c] = df[c].replace(values)

df = df.dropna()

y = df['Is Fraud?']
X = df.drop(['Is Fraud?'],axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
gnb = GaussianNB()
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)
print(classification_report(y_test, y_pred))