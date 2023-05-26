import sys
import pandas as pd 
import datetime
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
import torch
import Transaction

def transform_time(df_column):
    base_date = datetime.datetime(2023,5,5)
    timestamps = dict()
    for i in df_column:
        separed_time = str(i).split(':')
        time = datetime.time(int(separed_time[0]), int(separed_time[1]))
        combined_datetime = base_date.combine(base_date, time)
        timestamps[i] = datetime.datetime.timestamp(combined_datetime)
    return timestamps

def transform_amount(df_column):
    amounts = dict()
    for i in df_column:
        amounts[i] = float(str(i).split('$')[1])
    return amounts

def get_normalizer_dict(df_column):
    values = dict()
    count = 0
    for i in df_column:
        if values.get(i) is None:
            values[i] = count
            count += 1
    return values

def transform():
    df = pd.read_csv("data/filtered.csv")
    df.info()

    converted_time = transform_time(df['Time'])
    df['Time'] = df['Time'].replace(converted_time)

    converted_amounts = transform_amount(df['Amount'])
    df['Amount'] = df['Amount'].replace(converted_amounts)

    for c in ['Use Chip','Merchant City', 'Merchant State', 'Errors?', 'Is Fraud?']:
        df[c] = df[c].replace(get_normalizer_dict(df[c]))
    
    df = df.drop(['User'],axis=1)
    df = df.drop(['Card'],axis=1)
    df = df.drop(['Merchant State'],axis=1)
    df = df.drop(['Zip'],axis=1)
    df = df.drop(['MCC'],axis=1)
    df = df.drop(['Errors?'],axis=1)

    df['Year'] = df['Year'].fillna(df['Year'].mode()[0])
    df['Month'] = df['Month'].fillna(df['Month'].mode()[0])
    df['Day'] = df['Day'].fillna(df['Day'].mode()[0])
    df['Time'] = df['Time'].fillna(df['Time'].mode()[0])
    df['Amount'] = df['Amount'].fillna(df['Amount'].mean())
    df['Use Chip'] = df['Use Chip'].fillna(df['Use Chip'].mode()[0])
    df['Merchant Name'] = df['Merchant Name'].fillna(df['Merchant Name'].mode()[0])
    df['Is Fraud?'] = df['Is Fraud?'].fillna(df['Is Fraud?'].mode()[0])

    print("Check for Nan")
    for col in df.columns:
        if df[col].isnull().values.any():
            print(col)
    print("Check for Nan done!")
    return df

def train(df):
    y = df['Is Fraud?']
    X = df.drop(['Is Fraud?'], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 42, stratify=y)

    print("Naive Bayes....")
    model_gnb = GaussianNB()
    model_gnb.fit(X_train, y_train)

    y_pred = model_gnb.predict(X_test)
    print("Naive Bayes done!")

    evaluate(y_test, y_pred)
    return model_gnb
    
def evaluate(y_test, y_pred):
    print("Naive Bayes Report")
    print(confusion_matrix(y_test, y_pred))
    print("Acurácia: ", accuracy_score(y_test,y_pred))
    print("Precisão: ", precision_score(y_test,y_pred))

def save_model(model):
    torch.save(model, 'models/gnb.pt')

def get_model():
    return torch.load('models/gnb.pt')

def predict_gnb(t: Transaction.Transaction):
    model = get_model()
    return model.predict(t)

if __name__ == "__main__":
    df = transform()
    model = train(df)
    save_model(model)
else:
    sys.modules[__name__] = predict_gnb