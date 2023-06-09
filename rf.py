import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, precision_score
from sklearn.ensemble import RandomForestClassifier
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

    print('Random Forest Classifier....')
    model = RandomForestClassifier(random_state=42, n_jobs=-1, max_depth=20, class_weight='balanced', n_estimators=100, oob_score=True)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print('Random Forest Done')

    evaluate(y_test, y_pred)
    return model

def evaluate(y_test, y_pred):
    print('Random Forest Classifier')
    print(confusion_matrix(y_test, y_pred))
    print("Acurácia: ", accuracy_score(y_test,y_pred))
    print("Precisão: ", precision_score(y_test,y_pred))
    print("F1: ", f1_score(y_test,y_pred))

def get_model():
    return torch.load('models/rf.pt')

def save(model):
    torch.save(model,'models/rf.pt')

def predict_rf(t: Transaction.Transaction):
    model = get_model()
    return model.predict(t)

if __name__ == "__main__":
    df = pd.read_csv('data/transactions_final.csv')
    model = train(df)
    save(model)
else:
    sys.modules[__name__] = predict_rf
