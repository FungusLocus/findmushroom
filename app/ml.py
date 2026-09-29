import sklearn
import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn import datasets
from sklearn.metrics import accuracy_score

#skeleton for model

def train_model(dataset):

    X = dataset['features here']
    y = dataset['outcomes here']

    #test set size 33% of the whole sample
    test_size = 0.33
    
    #split data
    X_train, X_test, y_train, y_test =model_selection.train_test_split(X, y, test_size=test_size)
    
    #Model instance, classification with logistic regression
    model = LogisticRegression(class_weight='balanced')
    #fit model
    model.fit(X_train, y_train)
    
    #Evaluate model performance
    scoring = 'accuracy'
    results = model_selection.cross_val_score(model, X, y,
    scoring=scoring)
    print('Accuracy on validation set: %.2f%% (std = %.2f)' %
    (results.mean()*100, results.std()))
    #accuracy on test set
    result = model.score(X_test, y_test)
    print("Accuracy on test set: %.2f%%" % (result*100.0))