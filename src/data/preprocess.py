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

# create path to saved model: feature engineering, feature selection, SVR model
parent_path = Path(__file__).parent.parent.parent.resolve() # parent path
data_file_path = parent_path.joinpath('data/interim/test.csv') # path to data (TESTING)
saved_model_file_path = parent_path.joinpath('models/current/saved_step.pkl') # path to saved pickle model
engine_file_path = parent_path.joinpath('data/external/aircraft.csv')

# open pickle file and save its components into new variables
with open (saved_model_file_path, 'rb') as file:
    saved = pickle.load(file)

stored_engineering = saved['engineering']
stored_features = saved['features']
stored_model = saved['model']

# intial feature drop
def initial_drop_list(data):
    droplist = ['unit_number', 's_1', 's_5', 's_6', 's_10', 's_16', 's_18', 's_19']
    return data.drop(droplist, axis=1)

# feature engineering
def feature_engineering(data):
    data = initial_drop_list(data)
    return pd.DataFrame(stored_engineering.transform(data), 
             columns=stored_engineering.get_feature_names_out())

# feature selection
def feature_selection(data):
    engineered_data = feature_engineering(data)
    return engineered_data[stored_features]

# make RUL predictions
def make_prediction(data):
    preprocessed = feature_selection(data)
    return stored_model.predict(preprocessed)

# define the sensor names
def sensor_names():
    sensor_names = {"s_1":"(Fan inlet temperature) (◦R)",
                    "s_2":"(LPC outlet temperature) (◦R)",
                    "s_3":"(HPC outlet temperature) (◦R)",
                    "s_4":"(LPT outlet temperature) (◦R)",
                    "s_5":"(Fan inlet Pressure) (psia)",
                    "s_6":"(bypass-duct pressure) (psia)",
                    "s_7":"(HPC outlet pressure) (psia)",
                    "s_8":"(Physical fan speed) (rpm)",
                    "s_9":"(Physical core speed) (rpm)",
                    "s_10":"(Engine pressure ratio(P50/P2)",
                    "s_11":"(HPC outlet Static pressure) (psia)",
                    "s_12":"(Ratio of fuel flow to Ps30) (pps/psia)",
                    "s_13":"(Corrected fan speed) (rpm)",
                    "s_14":"(Corrected core speed) (rpm)",
                    "s_15":"(Bypass Ratio) ",
                    "s_16":"(Burner fuel-air ratio)",
                    "s_17":"(Bleed Enthalpy)",
                    "s_18":"(Required fan speed)",
                    "s_19":"(Required fan conversion speed)",
                    "s_20":"(High-pressure turbines Cool air flow)",
                    "s_21":"(Low-pressure turbines Cool air flow)"}

    return sensor_names

def engine_attributes(data):
    # get unique engine numbers from the user upload file
    engines_uploaded = data.unit_number.unique()




################################################################################
#data = pd.read_csv(data_file_path)#.drop(droplist, axis=1) # (TESTING)
#engines = pd.read_csv(engine_file_path)
#print(make_prediction(data))
#print(pd.DataFrame(sensor_names().items(), columns=['sensor', 'sensor_name']))
################################################################################