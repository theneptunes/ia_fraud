import sys
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
import datetime
import Transaction
import torch
import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, precision_score
import lightgbm as lgb
import Transaction
import torch

def train(df):
    X = df.drop('Is Fraud',axis=1)
    X = X.apply(pd.to_numeric, errors='coerce')

    scaler = StandardScaler()
    X_s = scaler.fit_transform(X)
    X_s = pd.DataFrame(X, columns=X.columns)

    y = df['Is Fraud']

    X_train, X_test, y_train, y_test = train_test_split(X_s, y, stratify=y, train_size=0.7, random_state=42)

    print('Logistic Regression....')
    model = LogisticRegression(solver='lbfgs', max_iter=400)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print('Logistic Regression Done')

    evaluate(y_test, y_pred)
    return model

def evaluate(y_test, y_pred):
    print('Logistic Regression')
    print(confusion_matrix(y_test, y_pred))
    print("Acurácia: {:.3f}".format(accuracy_score(y_test,y_pred)))
    print("Precisão: {:.3f}".format(precision_score(y_test,y_pred)))
    print("F1: {:.3f}".format(f1_score(y_test,y_pred)))

def get_model():
    return torch.load('models/lr.pt')

def save(model):
    torch.save(model,'models/lr.pt')

def predict_lr(t: Transaction.Transaction):
    model = get_model()
    return model.predict(t)

if __name__ == "__main__":
    df = pd.read_csv('data/transactions_final.csv')
    model = train(df)
    save(model)
else:
    sys.modules[__name__] = predict_lr
