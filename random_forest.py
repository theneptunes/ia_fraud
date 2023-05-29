import sys
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
import datetime
import Transaction
import torch

def transform():
    dataset_name = "data/filtered.csv"

    df = pd.read_csv(dataset_name)

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

    for c in ['Use Chip','Merchant City', 'Merchant State', 'Errors?']:
        values = {}
        count = 0
        for i in df[c]:
            if values.get(i) is None:
                values[i] = count
                count += 1
        df[c] = df[c].replace(values)

    #Normalização
    
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

    values = []
    for i in df['Is Fraud?']:
        if i == "No":
            values.append(False)
        else:
            values.append(True)
    df['Is Fraud?'] = values
    print("Check for Nan")
    for col in df.columns:
        if df[col].isnull().values.any():
            print(col)
    print("Check for Nan done!")
    df.info()
    return df

def train(df):
    y = df['Is Fraud?']

    X = df.drop(['Is Fraud?'],axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42, stratify=y)#sk metrics

    print('RF....')
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    y_pred=model.predict(X_test)
    print(len(y_test))
    print(len(y_pred))
    print("RF done!")

    evaluate(y_test, y_pred)
    return model

def evaluate(y_test, y_pred):
    # Avaliação
    #acurácia: quero que sempre que eu falar que é fraude, eu esteja certa
    #precisão: quero que sempre que for fraude, eu fale que é fraude
    print('RF')
    print(confusion_matrix(y_test, y_pred))
    print("Acurácia: ", accuracy_score(y_test,y_pred))
    print("Precisão: ", precision_score(y_test,y_pred))

def get_model():
    return torch.load('models/lr.pt')

def save(model):
    torch.save(model,'models/lr.pt')

def predict_lr(t :Transaction.Transaction):
    df = transform()
    #model = get_model()
    model = train(df)
    #save(model)
    return model.predict(t)

if __name__ == "__main__":
    df = transform()
    model = train(df)
    save(model)
else:
    sys.modules[__name__] = predict_lr