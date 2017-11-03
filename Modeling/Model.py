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

#Load LUT, features and
def load_LUT():
    thePathLut = '/Users/user/COMS-6998-REPO/FinalProject/'
    return pd.read_csv(thePathLut + 'predictorLUT.csv', index_col=0)  # ALGO LUT

def load_data():
    thePathLut = '/Users/user/COMS-6998-REPO/FinalProject/'
    df = pd.read_csv(thePathLut + 'combination_nadropped.csv')
    con = lite.connect('players.db')
    df = df.drop(['Team','Opp'], axis=1)
    df.to_sql("players_stats", con, if_exists='replace')
    return


def add_d():
    con = lite.connect('players.db')
    results = pd.read_sql_query("select year || week || team as comb, ProjPoints from players_stats where position = 'D' ", con)
    results.to_sql("temp", con, if_exists='replace')

    tempplay = pd.read_sql_query("select year || week || opponent as comb, player, position, team, salary, ownership, home, ProjPoints, minTweetCounts from players_stats", con)
    tempplay.to_sql("tempplay", con, if_exists='replace')

    d_points = pd.read_sql_query("select temp.ProjPoints as d_points, tempplay.player as play, tempplay.comb as date_opp, tempplay.team as team, tempplay.salary as salary, tempplay.ownership as ownership, tempplay.home as home, tempplay.ProjPoints as proj_points, tempplay.minTweetCounts as tweetcount from temp inner join tempplay on tempplay.comb = temp.comb",con)
    d_points.to_sql("master_table", con, if_exists='replace')
    return

def load_features():
    con = lite.connect('players.db')
    df1 = pd.read_sql_query("select * from master_table ", con)
    df1 = df1[['salary', 'proj_points','home','d_points']].copy()
    df1['salary'] = df1['salary'].str.replace(',', '')
    df1['salary'] = df1['salary'].str.replace('$', '')
    df1['salary'] = df1['salary'].astype(float)
    return df1

def load_target():
    con = lite.connect('players.db')
    df1 = pd.read_sql_query("select * from master_table ", con)
    return df1[['ownership']].copy()

#Return function call and grid search from LUT
def algoArray(theAlgo):
    theLUT = load_LUT()
    theAlgoOut = theLUT.loc[theAlgo, 'functionCall']
    return theAlgoOut

def gridSearch(theAlgo):
    theLUT = load_LUT()
    theAlgoOut = theLUT.loc[theAlgo, 'gridSearch']
    return theAlgoOut

#Optimize model from LUT using cross validation
def optModel():
    featureMatrix = load_features()
    fullIndex = load_target()

    theModels = ['OLS','RR','LR','EN','GBR','RFR','BR','ETR']
    theResults = pd.DataFrame(0, index=theModels, columns=['accuracy', 'confidence', 'runtime'])

    for theModel in theModels:
        startTime = time.time()
        model = eval(algoArray(theModel))
        print(theModel)

        # cross validation
        cvPerf = cross_val_score(model, featureMatrix, fullIndex, cv=10)
        theResults.loc[theModel, 'accuracy'] = round(cvPerf.mean(), 2)
        theResults.loc[theModel, 'confidence'] = round(cvPerf.std() * 2, 2)
        endTime = time.time()
        theResults.loc[theModel, 'runtime'] = round(endTime - startTime, 0)

    print(theResults)

    bestPerfStats = theResults.loc[theResults['accuracy'].idxmax()]
    modelChoice = theResults['accuracy'].idxmax()
    return modelChoice

#Optimize parameters
def optGrid(modelChoice):
    startTime = time.time()
    featureMatrix = load_features()
    fullIndex = load_target()

    model = eval(algoArray(modelChoice))
    grid = eval(gridSearch(modelChoice))
    grid.fit(featureMatrix, fullIndex)

    bestScore = round(grid.best_score_, 4)
    parameters = grid.best_params_
    endTime = time.time()
    print("Best Score: " + str(bestScore) + " and Grid Search Time: " + str(round(endTime - startTime, 0)))
    return parameters

#Opt
def optFunc(theAlgo, theParams):
    theLUT = load_LUT()
    theModel = theLUT.loc[theAlgo, 'optimizedCall']
    tempParam = list()
    for key, value in theParams.iteritems():
        tempParam.append(str(key) + "=" + str(value))
    theParams = ",".join(tempParam)
    theModel = theModel + theParams + ")"
    return theModel

#train OWNERSHIP model with optimal model and dump in pickle file
def ownershipTrain():
    featureMatrix = load_features()
    fullIndex = load_target()
    modelChoice = optModel()
    parameters = optGrid(modelChoice)

    startTime = time.time()
    model = eval(optFunc(modelChoice, parameters))  # train fully validated and optimized model
    model.fit(featureMatrix, fullIndex)
    # model.fit(train,trainIndex)
    joblib.dump(model, 'ownership.pkl')  # save model
    endTime = time.time()
    print("Model Save Time: " + str(round(endTime - startTime, 0)))


#Plot and evaluate correlation of features


