from sklearn.decomposition import PCA
import pandas as pd 
import plotly.express as px
import datetime
import numpy as np	
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.discriminant_analysis import StandardScaler 

dataset_name = "data/transactions_final.csv"

df = pd.read_csv(dataset_name)

y = df['Is Fraud']

X = df.drop(['Is Fraud'],axis=1)

sns.countplot(
    x='Is Fraud', 
    data=df)
plt.title('Fraud value count')
plt.show()

pca = PCA(n_components=14)
 	
# data scaling
x_scaled = StandardScaler().fit_transform(X)


# Fit and transform data
reduced_features = pca.fit_transform(x_scaled)
 
# Bar plot of explained_variance
plt.bar(
    range(1,len(pca.explained_variance_)+1),
    pca.explained_variance_
    )
 
plt.plot(
    range(1,len(pca.explained_variance_ )+1),
    np.cumsum(pca.explained_variance_),
    c='red',
    label='Cumulative Explained Variance')
 
plt.legend(loc='upper left')
plt.xlabel('Number of components')
plt.ylabel('Explained variance (eignenvalues)')
plt.title('Scree plot')
 
plt.show()
