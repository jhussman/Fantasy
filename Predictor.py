import numpy as np
import pandas as pd
import time
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from sklearn.linear_model import Ridge, Lasso, SGDRegressor, ElasticNet, LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import LinearSVR, SVR, NuSVR
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, BaggingRegressor, ExtraTreesRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import load_boston
from scipy import stats
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
#import matplotlib as plt
import os
import sqlite3 as lite


#Load pre-processed csv from fan duels
def load_fanduel():
    return pd.read_csv('/Users/user/COMS-6998-REPO/FinalProject/fanduel_current.csv')

#Make predictions for 1 player
def ownershipPredict(input):
    input = np.array(input).reshape(1,-1)
    path = '/Users/user/COMS-6998-REPO/FinalProject/'
    theFile = 'ownership.pkl'
    model = joblib.load(path + theFile)
    return model.predict(input)

def return_project():
    df = load_fanduel()
    output = list()
    for x in range(len(df)):
        input = [df.Salary[x], df.FPPG[x],df.Home[x],df.Opponent[x]]
        output.append(ownershipPredict(input))
    df['Predicted Ownership'] = np.array(output)
    return df
