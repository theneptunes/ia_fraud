# Dataset: https://www.kaggle.com/datasets/ealtman2019/credit-card-transactions?resource=download
# Code: https://www.kaggle.com/code/apoorvanitsureibm/lightgbm-on-credit-card-transactions/notebook
# 2nd code: https://www.kaggle.com/code/anoopnits/real-time-fraud-detection
import numpy as np 
import pandas as pd 
import os
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

df = pd.read_csv("./User0_credit_card_transactions.csv")

df.head()

for col in df.columns:
    col_type = df[col].dtype
    if col_type == 'object' or col_type.name == 'category':
        df[col] = df[col].astype('category')

y = df['Is Fraud?']

X = df.drop(['Is Fraud?'],axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0, stratify=y)

model = lgb.LGBMClassifier()
model.fit(X_train, y_train, feature_name='auto', categorical_feature = 'auto', verbose=50)

y_pred=model.predict(X_test)

# Avaliação
print(classification_report(y_test, y_pred))

#Possible Improvements
#Handle class imbalance
#Feature Engineering
#Create attributes from timestamp such as Hour, Minute and Day of the week
#Convert Amount column to float
#Do hyper-parameter tuning with creation on a validation set for the LightGBM Model
#Experiment with different types of Machine Learning Models and Deep Learning architectures for better outcomes