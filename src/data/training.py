# Full training (preprocessing: feature engineering, fearture selection; hyperparameter tuning, model run)
import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.feature_selection import SelectFromModel
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from mlxtend.feature_selection import ColumnSelector
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from pathlib import Path
import pickle

def training():
    # get training data
    path = Path(__file__).parent.parent.parent.resolve()
    filename = 'data/raw/train_FD001.txt'
    fullpath = path.joinpath(filename)
    index_names = ['unit_number', 'time_cycles']
    setting_names = ['setting_1', 'setting_2', 'setting_3']
    sensor_names = ['s_{}'.format(i+1) for i in range(0,21)]
    col_names = index_names + setting_names + sensor_names
    train = pd.read_csv(fullpath, sep='\s+',header=None,index_col=False,names=col_names)

    # initial feature selection
    train.drop(columns=['setting_1', 'setting_2', 'setting_3',  's_1', 's_5', 's_6', 
                        's_10', 's_16', 's_18', 's_19'], inplace=True)

    # add RUL
    def rul_func(df):    
        return df.groupby('unit_number')['time_cycles'].max()
        
    # some clean up on the training data
    temp = pd.DataFrame(rul_func(train)).reset_index()
    train = train.merge(temp, left_on='unit_number', right_on='unit_number')  
    train['RUL']=train['time_cycles_y']-train['time_cycles_x']
    train = train.rename(columns={'time_cycles_x': 'time_cycles'}) # rename to original
    train = train.drop('time_cycles_y', axis=1) # drop the max cycle column
    train = train.drop('time_cycles', axis=1)
    train = train.drop('unit_number', axis=1)

    # x,y
    # clip RUL in training data
    y_train = train.RUL.clip(upper=100)
    X_train = train.drop('RUL', axis=1)

    # feature engineering
    engineering_pipeline = make_pipeline(MinMaxScaler(),
                                        PolynomialFeatures(2))

    # fit and transform training data then transform test data
    X_train_fe = pd.DataFrame(engineering_pipeline.fit_transform(X_train), 
                            columns=engineering_pipeline.get_feature_names_out())

    # feature seletion
    svr = SVR(kernel='linear')
    svr.fit(X_train_fe, y_train) 

    select_features = SelectFromModel(svr, threshold='mean', prefit=True)
    select_features.get_support()
    feature_names = engineering_pipeline.get_feature_names_out()

    # top features to keep
    best_features = list(np.array(feature_names)[select_features.get_support()])

    # final datasets for modelling
    X_train_final = X_train_fe[best_features]

    # final model and tuning
    svr = SVR()

    # parameter tuning
    params = {'C': [0.1, 0.25, 0.50, 1.0], 
            'epsilon': [0.4, 0.3, 0.2, 0.1, 0.05],
            'kernel': ['rbf', 'linear']         
            }

    grid_search = RandomizedSearchCV(svr, 
                            param_distributions=params,
                            cv=5,
                            scoring='neg_root_mean_squared_error')


    grid_search.fit(X_train_final, y_train)

    model = grid_search.best_estimator_

    # store model and steps
    stored_data = {"model": model, "engineering": engineering_pipeline, "features": best_features}

    # save
    folder = 'models/current/'
    par_path = path.joinpath(folder)
    filename = 'saved_step2.pkl'
    fulpath = par_path.joinpath(filename)

    with open (fulpath, 'wb') as file:
        pickle.dump(stored_data, file)









