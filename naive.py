from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import pandas as pd 
from sklearn.metrics import classification_report

df = pd.read_csv("./User0_credit_card_transactions.csv")

df.drop(['User'],axis=1)
df.drop(['Card'],axis=1)
df.drop(['Merchant State'],axis=1)
df.drop(['Zip'],axis=1)
df.drop(['MCC'],axis=1)
df.drop(['Errors?'],axis=1)
df.drop(['Time'],axis=1)


df = df.dropna()

y = df['Is Fraud?']
X = df.drop(['Is Fraud?'],axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
gnb = GaussianNB()
gnb.fit(X_train, y_train)
y_pred = gnb.predict(X_test)
print(classification_report(y_test, y_pred))