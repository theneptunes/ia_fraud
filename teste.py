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

dataset_name = "./filtered.csv"

df = pd.read_csv(dataset_name)

print(df['Use Chip'].unique())

print(df['Merchant City'].unique())