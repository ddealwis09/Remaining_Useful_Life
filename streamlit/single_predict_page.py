import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from src.data.preprocess import feature_engineering, feature_selection, make_prediction
import streamlit as st
from PIL import Image
import pandas as pd
from pathlib import Path
import numpy as np


def single_predict():

    # page header
    st.header("RUL Simulator Page")

    # instructions text
    txt = st.text_area('Read me', "This feature is intended to give engineers a platform for simulating RUL for a single engine. The engineer can input sensor readings from a selected engine then vary the readings on a given sensor to provide inference on its impact on RUL.")

    required = ({"Intended user": "Core Engineering",
            "Method": "User selected engine and manual sensor entry",
            "Default": "Mean sensor reading in latest training run (all engines)",
            "Max": "Max sensor reading in latest training run plus 100 (all engines)"})
    st.write(required)

    # get unique aircraft numbers
    path = Path(__file__).parent.parent.resolve()
    aircraft_filename = 'data/external/aircraft.csv'
    fullpath = path.joinpath(aircraft_filename)
    aircraft_df = pd.read_csv(fullpath)
    aircraft_units = list(aircraft_df['unit_number'].unique())

    # user inputs
    engine_select = st.selectbox("Select aircraft ID", aircraft_units)

    # pull up aircraft information
    aircraft_selected = aircraft_df[aircraft_df['unit_number']==engine_select]
    st.dataframe(aircraft_selected)

    # bring in training data to get average sensor reading to intialize sliders
    path = Path(__file__).parent.parent.resolve()
    filename = 'data/raw/train_FD001.txt'
    fullpath = path.joinpath(filename)
    index_names = ['unit_number', 'time_cycles']
    setting_names = ['setting_1', 'setting_2', 'setting_3']
    sensor_names = ['s_{}'.format(i+1) for i in range(0,21)]
    col_names = index_names + setting_names + sensor_names
    train = pd.read_csv(fullpath, sep='\s+',header=None,index_col=False,names=col_names)
    # subset for user selected engine
    train = train[train.unit_number == engine_select]

    # calculate sensor average values as default for sliders
    means = []
    maxes = []
    for i in range(21):
        col_mean = train.iloc[:,i+5:i+6].mean()[0]
        col_max = train.iloc[:,i+5:i+6].max()[0]
        means.append(int(col_mean))
        maxes.append(int(col_max) + 100)

    # sensor inputs
    s1 = st.slider("Sensor 1 (Fan inlet temperature) (◦R)",0,maxes[0],means[0])
    s2 = st.slider("Sensor 2 (LPC outlet temperature) (◦R)",0,maxes[1],means[1])
    s3 = st.slider("Sensor 3 HPC outlet temperature) (◦R)",0,maxes[2],means[2])
    s4 = st.slider("Sensor 4 (Fan inlet temperature) (◦R)",0,maxes[3],means[3])
    s5 = st.slider("Sensor 5 (Fan inlet temperature) (◦R)",0,maxes[4],means[4])
    s6 = st.slider("Sensor 6 (Fan inlet temperature) (◦R)",0,maxes[5],means[5])
    s7 = st.slider("Sensor 7 (Fan inlet temperature) (◦R)",0,maxes[6],means[6]) 
    s8 = st.slider("Sensor 8 (Fan inlet temperature) (◦R)",0,maxes[7],means[7])
    s9 = st.slider("Sensor 9 (Fan inlet temperature) (◦R)",0,maxes[8],means[8])
    s10 = st.slider("Sensor 10 (Fan inlet temperature) (◦R)",0,maxes[9],means[9])
    s11 = st.slider("Sensor 11 (Fan inlet temperature) (◦R)",0,maxes[10],means[10])
    s12 = st.slider("Sensor 12 (Fan inlet temperature) (◦R)",0,maxes[11],means[11])
    s13 = st.slider("Sensor 13 (Fan inlet temperature) (◦R)",0,maxes[12],means[12])
    s14 = st.slider("Sensor 14 (Fan inlet temperature) (◦R)",0,maxes[13],means[13])
    s15 = st.slider("Sensor 15 (Fan inlet temperature) (◦R)",0,maxes[14],means[14])
    s16 = st.slider("Sensor 16 (Fan inlet temperature) (◦R)",0,maxes[15],means[15])
    s17 = st.slider("Sensor 17 (Fan inlet temperature) (◦R)",0,maxes[16],means[16])
    s18 = st.slider("Sensor 18 (Fan inlet temperature) (◦R)",0,maxes[17],means[17])
    s19 = st.slider("Sensor 19 (Fan inlet temperature) (◦R)",0,maxes[18],means[18])
    s20 = st.slider("Sensor 20 (Fan inlet temperature) (◦R)",0,maxes[19],means[19])
    s21 = st.slider("Sensor 21 (Fan inlet temperature) (◦R)",0,maxes[20],means[20])

    # create input vector for predictions
    cols = ['unit_number','s_1','s_2','s_3','s_4','s_5','s_6','s_7','s_8','s_9','s_10','s_11',
            's_12','s_13','s_14','s_15','s_16','s_17','s_18','s_19','s_20','s_21']

    X = [engine_select, s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s15,s17,s18,s19,s20,s21]
    X_df = pd.DataFrame([X], columns=cols)

    # make predictions
    predict_button = st.button("Predict!")
    if predict_button:
        st.write("Predicted RUL:", make_prediction(X_df))






    