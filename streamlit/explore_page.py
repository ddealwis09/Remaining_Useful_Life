import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from src.data.preprocess import feature_engineering, feature_selection, make_prediction
import streamlit as st
from PIL import Image
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def explore():
    # page header
    st.header("Explore Engine Degredation")

    @st.cache
    def loading():
        # get training data
        path = Path(__file__).parent.parent.resolve()
        filename = 'data/raw/train_FD001.txt'
        fullpath = path.joinpath(filename)
        index_names = ['unit_number', 'time_cycles']
        setting_names = ['setting_1', 'setting_2', 'setting_3']
        sensor_names = ['s_{}'.format(i+1) for i in range(0,21)]
        col_names = index_names + setting_names + sensor_names
        train = pd.read_csv(fullpath, sep='\s+',header=None,index_col=False,names=col_names)
        
        # add training RUL
        # calculate RUL for the training data
        def rul_func(df):    
            return df.groupby('unit_number')['time_cycles'].max()
        
        temp = pd.DataFrame(rul_func(train)).reset_index()
        train = train.merge(temp, left_on='unit_number', right_on='unit_number')  
        train['RUL']=train['time_cycles_y']-train['time_cycles_x']
        train = train.rename(columns={'time_cycles_x': 'time_cycles'}) # rename to original
        train = train.drop('time_cycles_y', axis=1) # drop the max cycle column

        # rename columns
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

        train.rename(columns=sensor_names, inplace=True)

        # get test data
        path = Path(__file__).parent.parent.resolve()
        filename = 'data/raw/test_FD001.txt'
        fullpath = path.joinpath(filename)
        index_names = ['unit_number', 'time_cycles']
        setting_names = ['setting_1', 'setting_2', 'setting_3']
        sensor_names = ['s_{}'.format(i+1) for i in range(0,21)]
        col_names = index_names + setting_names + sensor_names
        test = pd.read_csv(fullpath, sep='\s+',header=None,index_col=False,names=col_names).groupby('unit_number').last().reset_index()

        filename_rul = 'data/raw/RUL_FD001.txt'
        fullpath_rul = path.joinpath(filename_rul)
        rul = pd.read_csv(fullpath_rul, sep='\s+',header=None,index_col=False)

        return train, test, rul

    train = loading()[0]
    test = loading()[1]
    rul = loading()[2]

    # explore 1
    st.subheader("1. Single Engine Facet")
    st.text_area("Description", "Select a single aircraft and observe it's engine degregation (RUL) across all sensors", key=1)
    aircraft_units = list(train['unit_number'].unique())
    
    # user inputs
    engine_select = st.selectbox("Select aircraft ID", aircraft_units)

    # get unique aircraft numbers
    path = Path(__file__).parent.parent.resolve()
    aircraft_filename = 'data/external/aircraft.csv'
    fullpath = path.joinpath(aircraft_filename)
    aircraft_df = pd.read_csv(fullpath)
    aircraft_units = list(aircraft_df['unit_number'].unique())
    # pull up aircraft information
    aircraft_selected = aircraft_df[aircraft_df['unit_number']==engine_select]
    st.dataframe(aircraft_selected)

    # melt sensors
    subset = train.iloc[:, np.r_[0,1,26,5:26]]
    melted = pd.melt(subset, id_vars = subset.iloc[:,0:3], value_vars=subset.iloc[:,3:], 
                    var_name="sensor", value_name="reading")

    def sensorFacetPlot(df, unit_number):
        t = df[df['unit_number']==unit_number]
        g = sns.FacetGrid(t, col="sensor", col_wrap=4, sharex=False, sharey=False)
        g.map_dataframe(sns.regplot, x="RUL", y="reading", order=2, 
                        scatter=True, color='red', scatter_kws={"s": 80, "color": "lightblue", "edgecolor":"black"})

    st.pyplot(sensorFacetPlot(melted, engine_select)), melted

    # explore 2
    st.subheader("2. Single Sensor Facet")
    st.text_area("Description", "Select a single sensor and observe it's engine degregation (RUL) across all aircrafts", key=2)
    aircraft_sensors = list(melted['sensor'].unique())

    # user inputs
    sensor_select = st.selectbox("Select a sensor", aircraft_sensors)

    def engineFacetPlot(df, sensor):
        t = df[df['sensor']==sensor]
        g = sns.FacetGrid(t, col="unit_number", col_wrap=4, sharex=False, sharey=False)
        g.map_dataframe(sns.regplot, x="RUL", y="reading", order=2, 
                        scatter=True, color='red', scatter_kws={"s": 80, "color": "lightblue", "edgecolor":"black"})

    st.pyplot(engineFacetPlot(melted, sensor_select)), melted

    # explore 3
    st.subheader("3. Test Set Predictions vs Actual")
    st.text_area("Description", "Observe the model's performance vs actual RUL on the hold-out data set", key=3)

    test_features = test.iloc[:,np.r_[0,5:26]]
    test_features['predicted'] = make_prediction(test_features)
    test_features['actual'] = rul
    test_features['abs error (%)'] = abs(test_features.actual/test_features.predicted - 1) * 100
    final = test_features.iloc[:,np.r_[0,22:25]]

    # determine threshold
    max = int(final['abs error (%)'].max())

    threshold = st.slider('Set threshold absolute error (%) to filter on:', 0, max, 1)
    filter = st.radio( "Do you want to filter predictions for engines only above or at your error threshold?", ('Yes', 'No'))

    if filter == "Yes":
        filtered = final[final['abs error (%)'] >= threshold]
        st.write("Total number of engines above threshold:", len(filtered))
        #mean_error = round(filtered['abs error (%)'].mean(),1)
        #st.write("Mean error of filtered engines:", mean_error)
        st.dataframe(filtered)

        # plot distribution
        fig, ax = plt.subplots()
        fig.set_size_inches(3, 3)
        plot = sns.histplot(x=filtered['abs error (%)'], kde=True, ax=ax)
        plt.title('Error distrbution')
        st.pyplot(plot.figure)
    else:
        st.write("Total number of engines:", len(final))
        #mean_error = round(final['abs error (%)'].mean(),1)
        #st.write("Mean error of filtered engines:", mean_error)
        st.dataframe(final)

        # plot distribution
        fig, ax = plt.subplots()
        fig.set_size_inches(3, 3)
        plot = sns.histplot(x=final['abs error (%)'], kde=True, ax=ax)
        plt.title('Error distrbution')
        st.pyplot(plot.figure)

        