from sklearn.decomposition import PCA
import pandas as pd 
import datetime

dataset_name = "data/clean.csv"

df = pd.read_csv(dataset_name)

#df = df.drop(['Teste'], axis=1)
#df.to_csv('data/clean.csv')

y = df['Is Fraud?']

X = df.drop(['Is Fraud?'],axis=1)


pca = PCA(n_components=2)
pca.fit(X)

print(X.columns)

print(pca.components_)

print(pca.explained_variance_)