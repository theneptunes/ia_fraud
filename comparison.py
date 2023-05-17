import numpy as np 
import pandas as pd 
import os
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import datetime

dataset_name = "./filtered.csv"

df = pd.read_csv(dataset_name)
df.info()

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
    amounts[i] = float(str(i).split('$')[1])
df['Amount'] = df['Amount'].replace(amounts)

for c in ['Use Chip','Merchant City', 'Merchant State', 'Errors?', 'Is Fraud?']:
    values = {}
    count = 0
    for i in df[c]:
        if values.get(i) is None:
            values[i] = count
            count += 1
    df[c] = df[c].replace(values)

#Normalização
df['User'] = df['User'].fillna(df['User'].mode()[0])
df['Card'] = df['Card'].fillna(df['Card'].mode()[0])
df['Year'] = df['Year'].fillna(df['Year'].mode()[0])
df['Month'] = df['Month'].fillna(df['Month'].mode()[0])
df['Day'] = df['Day'].fillna(df['Day'].mode()[0])
df['Time'] = df['Time'].fillna(df['Time'].mode()[0])
#df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df['Amount'] = df['Amount'].fillna(df['Amount'].mean())#.fillna(df['Amount'].shift() + df['Amount'].shift(-1)/2)
#df.dropna(subset = ['Amount'])
df['Use Chip'] = df['Use Chip'].fillna(df['Use Chip'].mode()[0])
df['Merchant Name'] = df['Merchant Name'].fillna(df['Merchant Name'].mode()[0])
df['Merchant City'] = df['Merchant City'].fillna(df['Merchant City'].mode()[0])
df['Merchant State'] = df['Merchant State'].fillna(df['Merchant State'].mode()[0])
df['Zip'] = df['Zip'].fillna(df['Zip'].mode()[0])
df['MCC'] = df['MCC'].fillna(df['MCC'].mode()[0])
df['Errors?'] = df['Errors?'].fillna(df['Errors?'].mode()[0])
df['Is Fraud?'] = df['Is Fraud?'].fillna(df['Is Fraud?'].mode()[0])

print("Check for Nan")
for col in df.columns:
    if df[col].isnull().values.any():
        print(col)
print("Check for Nan done!")

df.info()
y = df['Is Fraud?']

X = df.drop(['Is Fraud?'],axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 42, stratify=y)

print('LGBM....')
model_lgbm = lgb.LGBMClassifier()
model_lgbm.fit(X_train, y_train, feature_name='auto', categorical_feature = 'auto', verbose=50)

y_pred_lgbm=model_lgbm.predict(X_test)
print("LGBM done!")

print("Logictic regression....")
model_lr = LogisticRegression(solver='lbfgs', max_iter=400)
model_lr.fit(X_train, y_train)

y_pred_lr=model_lr.predict(X_test)
print("Logictic regression done!")

#print("Random forest....")
#model_rf = RandomForestClassifier(n_estimators = 100)
#model_rf.fit(X_train, y_train)

#y_pred_rf=model_rf.predict(X_test)
#print("Random forest done!")

#print("Isolation forest....")
#model_if = IsolationForest(contamination='auto', random_state=42)
#model_if.fit(X_train, y_train)

#y_pred_if=model_if.predict(X_test)
#y_pred_if = ['Yes' if i==-1 else 'No' for i in y_pred_if]

#print("Isolation forest done!")

# Avaliação
print('LGBM Report')
print(classification_report(y_test, y_pred_lgbm))
importances = model_lgbm.feature_importances_
importances_greater_than_zero = []
for i in importances:
    if i > 0:
        importances_greater_than_zero.append(i)
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(X.columns, importances_greater_than_zero)]
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
print()
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];


print('Logistic regression Report')
print(classification_report(y_test, y_pred_lr))

#print('Random Forest Report')
#print(classification_report(y_test, y_pred_rf))
#importances = model_rf.feature_importances_
#importances_greater_than_zero = []
#for i in importances:
#    if i > 0:
#        importances_greater_than_zero.append(i)
#feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(X.columns, importances_greater_than_zero)]
#feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
#print()
#[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];

#print('Isolation Tree Report')
#print(classification_report(y_test, y_pred_if))
#print("For this model, there isn't an impemented logic for calc feature importance")