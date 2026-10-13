import sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from build_dataset import create_training_set, make_prediction_table_for_grids
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
    # print(models)
    return models


def logistic_regression(X,y,w):
    test_size = 0.2
    X_train, X_test, y_train, y_test, w_train, w_test =train_test_split(X, y, w, test_size=test_size)
    model = LogisticRegression(class_weight='balanced')
    model.fit(X_train, y_train, sample_weight=w_train)
    
    probs = model.predict_proba(X_test)[:, 1]
    print("AUC:", round(roc_auc_score(y_test, probs),2))
    print("PR-AUC:", round(average_precision_score(y_test, probs),2))
    
    cv_scores = cross_val_score(model, X, y, scoring='roc_auc', params={'sample_weight': w.values})
    print('CV AUC: %.2f (std = %.2f)' % (cv_scores.mean(), cv_scores.std()))
    
    result = model.score(X_test, y_test)
    print("Accuracy on test set: %.2f%%" % (result*100.0))
    
    coef_df = pd.DataFrame({'Feature': X.columns,'Coefficient': model.coef_[0]})
    print("\n--- Model Coefficients ---")
    print(coef_df)
    return model
    

def make_predictions():
    features = ['prec', 'temp', 'prec_7d', 'prec_14d', 'temp_7d', 'temp_14d']
    full_grid = make_prediction_table_for_grids()
    X = full_grid[features]
    models = train_model()
    for species, model in models.items():
        full_grid[f"prob_{species}"] = model.predict_proba(X)[:, 1]
    
    # print(full_grid)
    # full_grid.to_csv("datasets/predictions.csv", index=False)
    # print(full_grid.columns)
    return full_grid

def predictions_for_db():
    df = make_predictions()
    # print(df['Station'].nunique())
    df = df.drop(columns=['geometry', 'Station', 'prec', 'temp', 'prec_7d', 'prec_14d', 'temp_7d', 'temp_14d', ])
    mushrooms = ['herkkutatti', 'karvarousku', 'keltavahvero', 'korvasieni', 'lampaankääpä', 'mustatorvisieni', 'mustavahakas', 'sikurirousku', 'suppilovahvero', 'vaaleaorakas']
    columns = [f"prob_{s}" for s in mushrooms]
    long_df = df.melt(id_vars=['grid_x', 'grid_y', 'week'], value_vars=columns, var_name='species', value_name='probability')
    long_df['species'] = long_df['species'].str.replace('prob_', '', regex=False)
    # in Python, check how many land cells exist for one species/week
    print(long_df[(long_df["species"] == "herkkutatti") & (long_df["week"] == 36)].shape[0])
    
    return long_df
    

if __name__ == "__main__":
    # make_predictions()
    predictions_for_db()