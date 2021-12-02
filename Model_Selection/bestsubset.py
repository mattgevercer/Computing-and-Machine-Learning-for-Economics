# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 11:14:33 2020

@author: Matt
"""
import itertools
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.datasets import fetch_california_housing
import pandas as pd

def bestsubset(X,y): 
    mse=np.empty(0) # contains the best training mse for each of the model with k X's
    cs=[] #contains the included predictors for each model under consideration
    for k in range(X.shape[1]):
        # creates all possible models with k predictors
        mse_k = []
        cs_k = []
        for c in itertools.combinations(range(X.shape[1]),k+1):
            #sets Xc to be the correct X matrix given the chosen predictors for that iteration of the loop.
            Xc=X.iloc[:,list(c)]
            model=LinearRegression()
            model.fit(Xc,y)
            y_pred=model.predict(Xc)
            score = -mean_squared_error(y,y_pred)
            mse_k.append(score)
            cs_k.append(c)
        mse=np.append(mse, max(mse_k))
        cs.append(cs_k[mse_k.index(max(mse_k))])
    mse_cv = np.empty(0)
    for i in cs:
        Xc=X.iloc[:,list(i)]
        scores=cross_val_score(LinearRegression(),
                               Xc,
                               y,
                               cv=KFold(5,shuffle=True,random_state=0),
                               scoring="neg_mean_squared_error")
        mse_cv=np.append(mse_cv,np.mean(scores))
    i=np.argmax(mse_cv) #find model with biggest MSE (ith model in the list)
    Xc=X.iloc[:,list(cs[i])] #subset x's based on line above
    model=LinearRegression()
    model.fit(Xc,y) #fit model based on optimal predictors
    model.coef_
    ret = [list(cs[i]),model.coef_]
    return ret

def subset(t, l):
    """
    Parameters
    ----------
    t : Tuple
        Indexes of columns in a dataframe
    l : list
        List of tuples of indexes of a dataframe
    Returns a subsetted list containing tuples that include values in input tuple
    -------
    """
    keep = l.copy()
    for i in t:
        for j in reversed(range(len(keep))):
            if i not in keep[j]:
                keep.pop(j)
    return keep

def forwardsubset(X,y):
    mse=np.empty(0) # contains the best training mse for each of the model with k X's
    cs=[] #contains the included predictors for each model under consideration
    #best_k =[] # contains index of best 
    k = [i for i in itertools.combinations(range(X.shape[1]),1)]
    mse_1 = []
    cs_1 = []
    #find best model with k=1
    for i in k: 
        Xc=X.iloc[:,list(i)]
        model=LinearRegression()
        model.fit(Xc,y)
        y_pred=model.predict(Xc)
        score = -mean_squared_error(y,y_pred)
        mse_1.append(score)
        cs_1.append(i)
    mse=np.append(mse, max(mse_1))
    cs.append(cs_1[mse_1.index(max(mse_1))])
    #find best models with k = 2,3,4,etc...
    for r in range(2, len(X.columns)+1):
         k = [i for i in itertools.combinations(range(X.shape[1]),r)]
         sub = subset(cs[-1],k)#subset based on prev best predictors
         mse_k = []
         cs_k = []
         for q in sub: #iterate through subsetted column combos
            Xc=X.iloc[:,list(q)]
            model=LinearRegression()
            model.fit(Xc,y)
            y_pred=model.predict(Xc)
            score = -mean_squared_error(y,y_pred)
            mse_k.append(score)
            cs_k.append(q) 
         mse=np.append(mse, max(mse_k))
         cs.append(cs_k[mse_k.index(max(mse_k))])
    mse_cv = np.empty(0)
    for i in cs:
        Xc=X.iloc[:,list(i)]
        scores=cross_val_score(LinearRegression(),
                               Xc,
                               y,
                               cv=KFold(5,shuffle=True,random_state=0),
                               scoring="neg_mean_squared_error")
        mse_cv=np.append(mse_cv,np.mean(scores))
    i=np.argmax(mse_cv) #find model with biggest MSE (ith model in the list)
    Xc=X.iloc[:,list(cs[i])] #subset x's based on line above
    model=LinearRegression()
    model.fit(Xc,y) #fit model based on optimal predictors
    model.coef_
    ret = [list(cs[i]),model.coef_]
    return ret

housing=fetch_california_housing()
x=pd.DataFrame(housing.data)
y=housing.target
pred_names= housing.feature_names
sub1 = forwardsubset(x,y)
sub2 = bestsubset(x,y)
best_predictors1 = [pred_names[i] for i in sub1[0]]
best_predictors2 = [pred_names[i] for i in sub2[0]]
print("The best predictors given by the bestsubset algorithm for median house price in a Califoria district are: %s" % best_predictors1)
print("The best predictors given by the forwardsubset algorithm for median house price in a Califoria district are: %s" % best_predictors2)
