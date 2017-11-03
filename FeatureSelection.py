from Model import load_target, load_features
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

def corr():
    X = load_features()
    y = load_target()
    cols = list(X)
    for i in range(len(cols)):
        print cols[i], pearsonr(np.array(X.iloc[:,i]).ravel(),np.array(y).ravel())[0]

def salary_plot():
    X = load_features()['salary']
    y = load_target()
    plt.figure()
    plt.scatter(X,y,s=3, color='red')
    plt.xlabel('Salary [$]')
    plt.ylabel('Ownership Percentage [%]')
    plt.title('Salary')
    plt.show()
    plt.savefig('/Users/user/COMS-6998-REPO/FinalProject/FeaturePlots/salary.eps', format='eps', dpi=1000)

def twitter_plot():
    X = load_features()['tweetcount']
    y = load_target()
    plt.figure()
    plt.scatter(X,y,s=3, color='blue')
    plt.xlabel('Tweet Count')
    plt.ylabel('Ownership Percentage [%]')
    plt.title('Tweet Count')
    plt.show()
    plt.savefig('/Users/user/COMS-6998-REPO/FinalProject/FeaturePlots/tweet.eps', format='eps', dpi=1000)

def propoints_plot():
    X = load_features()['proj_points']
    y = load_target()
    plt.figure()
    plt.scatter(X,y,s=3, color='green')
    plt.xlabel('Projected Points')
    plt.ylabel('Ownership Percentage [%]')
    plt.title('Projected Points')
    plt.show()
    plt.savefig('/Users/user/COMS-6998-REPO/FinalProject/FeaturePlots/points.eps', format='eps', dpi=1000)

def home_plot():
    X = load_features()['home']
    y = load_target()
    plt.figure()
    plt.scatter(X,y,s=3, color='black')
    plt.xlabel('Home or Away')
    plt.ylabel('Ownership Percentage [%]')
    plt.title('Home or Away')
    plt.show()
    plt.savefig('/Users/user/COMS-6998-REPO/FinalProject/FeaturePlots/home.eps', format='eps', dpi=1000)

def dpoints_plot():
    X = load_features()['d_points']
    y = load_target()
    plt.figure()
    plt.scatter(X,y,s=3, color='black')
    plt.xlabel('Number of Projected Points for Opposing Defense')
    plt.ylabel('Ownership Percentage [%]')
    plt.title('Number of Projected Points for Opposing Defense')
    plt.show()
    plt.savefig('/Users/user/COMS-6998-REPO/FinalProject/FeaturePlots/d_points.eps', format='eps', dpi=1000)


