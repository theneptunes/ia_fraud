import sys
#https://towardsdatascience.com/random-forest-in-python-24d0893d51c0

# Use numpy to convert to arrays
import numpy as np
import pandas as pd
# Using Skicit-learn to split data into training and testing sets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def get_data():
    #1. One-hot encoded categorical variables
    #2. Split data into features and labels
    #3. Converted to arrays
    #4. Split data into training and testing sets
    features = pd.read_csv('transacoes.csv')
    features= features.drop('Nome_completo', axis = 1)
    features.head(5)
    # One-hot encode the data using pandas get_dummies
    features = pd.get_dummies(features)
    # Display the first 5 rows of the last 12 columns
    features.iloc[:,5:].head(5)
    #features['Horario'] = features['Horario'].map({'Dia':0,'Noite':1, 'Tarde': 2})
    # Labels are the values we want to predict
    labels = np.array(features['Fraude'])
    #print(labels)
    #1 é fraude, 0 não é fraude
    # Remove the labels from the features
    # axis 1 refers to the columns
    features= features.drop('Fraude', axis = 1)
    # Saving feature names for later use
    feature_list = list(features.columns)
    # Convert to numpy array
    features = np.array(features)
    #print(features)

    # Split the data into training and testing sets
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25)

    print('Training Features Shape:', train_features.shape)
    print('Training Labels Shape:', train_labels.shape)
    print('Testing Features Shape:', test_features.shape)
    print('Testing Labels Shape:', test_labels.shape)

    return train_features, test_features, train_labels, test_labels, feature_list
# The baseline predictions are the historical averages
#baseline_preds = test_features[:, feature_list.index('average')]
# Baseline errors, and display average baseline error
#baseline_errors = abs(baseline_preds - test_labels)
#print('Average baseline error: ', round(np.mean(baseline_errors), 2))

def train(train_features, test_features, train_labels, test_labels):
    # Instantiate model with x decision trees
    rf = LogisticRegression(solver='lbfgs', max_iter=400)
    # Train the model on training data
    rf.fit(train_features, train_labels)

    return rf

def test(rf, test_features, test_labels):
    # Use the forest's predict method on the test data
    predictions = rf.predict(test_features)
    # Calculate the absolute errors
    errors = abs(predictions - test_labels)
    # Print out the mean absolute error (mae)
    print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')
    # Calculate mean absolute percentage error (MAPE)
    #Não funciona porque são variáveis categóricas
    #mape = 100 * (errors / test_labels)
    # Calculate and display accuracy
    #accuracy = 100 - np.mean(mape)
    accuracy = accuracy_score(test_labels, predictions) * 100
    print('Accuracy:', round(accuracy, 2), '%.')

#Visualize
# Import tools needed for visualization
#from sklearn.tree import export_graphviz
#import pydot

# Pull out one tree from the forest
#tree = rf.estimators_[5]
# Export the image to a dot file
#export_graphviz(tree, out_file = 'tree.dot', feature_names = feature_list, rounded = True, precision = 1)
# Use dot file to create a graph
#(graph, ) = pydot.graph_from_dot_file('tree.dot')
# Write graph to a png file
#graph.write_png('tree.png')

# Limit depth of tree to 3 levels
#rf_small = RandomForestRegressor(n_estimators=10, max_depth = 3)
#rf_small.fit(train_features, train_labels)
# Extract the small tree
#tree_small = rf_small.estimators_[5]
# Save the tree as a png image
#export_graphviz(tree_small, out_file = 'small_tree.dot', feature_names = feature_list, rounded = True, precision = 1)
#(graph, ) = pydot.graph_from_dot_file('small_tree.dot')
#graph.write_png('small_tree.png');

def calc_importance(rf, feature_list):
    #how much including a particular variable improves the prediction
    # Get numerical feature importances
    importances = list(rf.feature_importances_)
    # List of tuples with variable and importance
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
    # Sort the feature importances by most important first
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
    # Print out the feature and importances 
    print()
    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];
#curva de precisão-recall
def logistic_progression(localizacao, valor, periodo, categoria):
    train_features, test_features, train_labels, test_labels, feature_list = get_data()
    rf = train(train_features, test_features, train_labels, test_labels)
    test(rf, test_features, test_labels)
    my_array = [valor, False, False, False, False, False, False, False, False, False]
    if localizacao == 'Recife-PE':
        my_array[1] = True
    elif localizacao == 'Campinas-SP':
        my_array[5] = True
    elif localizacao=='São Paulo-SP':
        my_array[6] = True
    else:
        my_array[9] = True
    
    if periodo == 'Noite':
        my_array[2] = True
    elif periodo == 'Dia':
        my_array[7] = True
    else:
        my_array[8] = 'Tarde'

    if categoria=='Comida':
        my_array[3] = True
    elif categoria=='Eletronico':
        my_array[4] = True
    #test(rf, test_features, test_labels)
    #calc_importance(rf, feature_list)
    predicted = rf.predict([my_array])
    return predicted

sys.modules[__name__] = logistic_progression