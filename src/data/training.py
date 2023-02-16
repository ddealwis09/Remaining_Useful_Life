# Full training (preprocessing: feature engineering, fearture selection; hyperparameter tuning, model run)
import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path
import pickle

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
train.drop(columns=['setting_1', 'setting_2', 'setting_3',  's_1', 's_5', 's_6', 's_10', 's_16', 's_18', 's_19'], inplace=True)

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

# feature engineering









