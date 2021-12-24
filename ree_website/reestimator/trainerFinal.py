#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Import packages
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, RandomizedSearchCV, KFold
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression , Ridge , Lasso
from sklearn.metrics import mean_absolute_percentage_error as mape
from sklearn.metrics import mean_squared_error as rmse

from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

import xgboost as xgb
from xgboost.sklearn import XGBRegressor
from xgboost import plot_importance


class Trainer():
    """ Initialize dataframe
    """
    def __init__(self, df, col_list, target_var,
                 scaler,model,params_cv, randomsearch_dict,
                                   nsplits = 10,
                                   scor = "neg_mean_absolute_error"):

        self.df = df
        self.col_list = col_list
        self.target_var = target_var
        self.scaler = scaler
        self.model = model
        self.params_cv = params_cv
        self.randomsearch_dict = randomsearch_dict
        self.nsplits = nsplits
        self.scor = scor

    def define_dataset(self, df, col_list, target_var):
        # define dataset
        y = self.df[self.target_var]
        X = self.df[self.col_list]
        return X,y


    def holdout(self, X, y):
        """ Instantiating train test split while creating
        X and y train and test variables
        """
        #X,y = self.define_dataset(self.df, self.col_list, self.target_var)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size = 0.3, random_state = 0)

        return X_train, X_test, y_train, y_test

    def scale(self, X_train, X_test):
        """instantiating the scaler
        scaling Xs"""

        #X_train, X_test, y_train, y_test = self.split_X_y_sets()
        self.scaler.fit(X_train)
        X_train_sc = self.scaler.transform(X_train)
        X_test_sc = self.scaler.transform(X_test)

        return X_train_sc, X_test_sc #, y_train, y_test


    def set_model(self, model):

        """defines the model as a class attribute"""
        '''returns a model'''
        if self.model=="Lasso":
            modelo = Lasso()
        elif self.model=="Ridge":
            modelo = Ridge()
        elif self.model == "RandomForest":
            modelo = RandomForestRegressor(random_state = 42)
        else:
            if self.model == "XGBoost":
                #modelo = xgb.XGBRegressor()
                modelo = xgb.XGBRegressor(booster = 'gbtree', objective ='reg:squarederror',
                                                colsample_bytree = 0.3, learning_rate = 0.35,
                                      max_depth = 10, alpha = 0.1, n_estimators = 500)


        return modelo



    def evaluate(self, model, X_train, X_test, y_train, y_test):
        """evaluates the pipeline on df_test and return the RMSE"""

        model.fit(X_train,y_train)
        y_pred = model.predict(X_test)
        R2 = 100*(r2_score(y_test, y_pred))
        MAE = round(mape(y_test, y_pred), 2)
        RMSE = round(rmse(y_test, y_pred), 2)

        res = {'Model': self.model, 'R2' : R2, 'MAE': MAE, 'RMSE': RMSE}
        return res


    def get_feature_importances(self):
        """evaluates the pipeline on df_test and return the RMSE"""
        X,y = self.define_dataset(self.df, self.col_list, self.target_var)

        # execute search
        search = self.set_Randomized_search(self.model)

        X_train, X_test, y_train, y_test= self.holdout(X, y)
        X_train_sc, X_test_sc = self.scale(X_train, X_test)
        res = search.fit(X_train_sc, y_train)

        #model = self.set_model(self.model)


        if (self.model == "Lasso") | (self.model == "Ridge"):

            model = self.set_model(self.model)
            best = model.set_params(**res.best_params_)
            best.fit(X_train_sc,y_train)
            features = best.coef_

        else:
            #RandomForest or XGBoost
            model = self.set_model(self.model)
            best = model.set_params(**res.best_params_)
            best.fit(X_train_sc,y_train)
            features = pd.DataFrame(best.feature_importances_,
                        index = X_train.columns,
                    columns=['importance']).sort_values('importance', ascending=False)

        return features

    def set_Randomized_search(self, model):


        if (self.model == "Lasso") | (self.model == "Ridge"):

            model = self.set_model(self.model)

            # define cross validation
            cv = KFold(n_splits=self.nsplits)

            search_case = RandomizedSearchCV(model, self.params_cv,
                                        n_iter=self.randomsearch_dict['reg_iter'],
                                            scoring= self.scor, n_jobs=-1,
                                                cv=cv, random_state=1)

        else:
            if self.model == "RandomForest":

                random_forest = self.set_model(self.model)

                #random_forest = RandomForestRegressor(random_state = 42)

                search_case = RandomizedSearchCV(estimator = random_forest,
                                                 param_distributions = self.params_cv,
                   n_iter = self.randomsearch_dict['forest_iter'],
                                                 cv = 5, verbose=2, random_state=42, n_jobs = -1)

            else:
                print("**333*** ", model)

                xgboost_regression = self.set_model(self.model)

                search_case = RandomizedSearchCV(estimator = xgboost_regression,
                                       param_distributions = self.params_cv,
                                       n_iter = self.randomsearch_dict['xgboost_iter'],
                                                 cv = 3, verbose=2, #n_iter=1000
                                       random_state=0, n_jobs = -1)

        return search_case


    def execute(self):

        X,y = self.define_dataset(self.df, self.col_list, self.target_var)

        # execute search
        search = self.set_Randomized_search(self.model)

        X_train, X_test, y_train, y_test= self.holdout(X, y)
        X_train_sc, X_test_sc = self.scale(X_train, X_test)
        res = search.fit(X_train_sc, y_train)

         # summarize result
        print('Best Score: %s' % res.best_score_)
        print('Best Hyperparameters: %s' % res.best_params_)

        model = self.set_model(self.model)

        best = model.set_params(**res.best_params_)
        #print("model  ", model)

        # train and predict
        result = self.evaluate(best, X_train_sc, X_test_sc, y_train, y_test)

        return result
