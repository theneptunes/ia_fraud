import numpy as np 
import pandas as pd 
import os
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import datetime

def get_normalizer_dict(df_column):
    values = dict()
    count = 0
    for i in df_column:
        if values.get(i) is None:
            values[i] = count
            count += 1
    return values

dataset_name = "../data/filtered.csv"

df = pd.read_csv(dataset_name)

# print(df['Use Chip'].unique())

# print(df['Merchant City'].unique())

for c in ['Use Chip','Merchant City', 'Merchant State', 'Errors?', 'Is Fraud?']:
    df[c] = df[c].replace(get_normalizer_dict(df[c]))
    print(df[c])