import sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from build_dataset import create_training_set
from sklearn.metrics import roc_auc_score, average_precision_score


def train_model():
    models = {}
    data = create_training_set()
    for specie in data:
        print(specie)
        X = data[specie][['prec', 'temp', 'prec_7d', 'prec_14d', 'temp_7d', 'temp_14d']]
        y = data[specie]['observed']
        sample_weight = 1 / (1 + data[specie]['distance_meters'] / 10000)
        result = logistic_regression(X, y, sample_weight)
        models[specie] = result
    print(models)

        

def logistic_regression(X,y,w):
    test_size = 0.2
    X_train, X_test, y_train, y_test, w_train, w_test =train_test_split(X, y, w, test_size=test_size)
    model = LogisticRegression(class_weight='balanced')
    model.fit(X_train, y_train, sample_weight=w_train)
    
    probs = model.predict_proba(X_test)[:, 1]
    print("AUC:", roc_auc_score(y_test, probs))
    print("PR-AUC:", average_precision_score(y_test, probs))
    
    cv_scores = cross_val_score(model, X, y, scoring='roc_auc', params={'sample_weight': w.values})
    print('CV AUC: %.3f (std = %.3f)' % (cv_scores.mean(), cv_scores.std()))
    
    result = model.score(X_test, y_test)
    print("Accuracy on test set: %.2f%%" % (result*100.0))
    return model
    

        

    

if __name__ == "__main__":
    train_model()