import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from src.data.preprocess import feature_engineering, feature_selection, make_prediction
import streamlit as st
from PIL import Image
import pandas as pd
from pathlib import Path

def bulk_upload():

    # page header
    st.header("Bulk Turbofan Upload Page")

    # file metadata
    required = ({"Intended user": "Maintenance and Engineering",
                "File Type": "CSV", 
                "Required metadata": "Engine unit number", 
                "Required data": "21 aircraft sensor readings",
                "Expected number of columns": 22})
    st.write(required)

    # file uploader
    uploaded_file = st.file_uploader("Choose a CSV file for bulk engine upload")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # preview of upload for user 
        sample = df.head(5)
        st.write("Preview of your file:")
        st.dataframe(sample)
    
        # preserve original upload engine unit numbers (to join to aircraft data)
        units = df['unit_number'].unique()

        # set threshold slider
        threshold = st.slider('Set RUL threshold for maintenance (days):', 0, 150, 100)

        # allow user to filter for items at or below threshold prediction
        filter = st.radio( "Do you want to filter predictions for engines only below or at your RUL threshold?", ('Yes', 'No'))

        # make predictions on input data
        predictions_df = pd.DataFrame(make_prediction(df), columns=['RUL'])
        
        # aircraft information
        path = Path(__file__).parent.parent.resolve()
        aircraft_filename = 'data/external/aircraft.csv'
        fullpath = path.joinpath(aircraft_filename)
        aircraft_df = pd.read_csv(fullpath)
        aircraft_filtered = aircraft_df[aircraft_df['unit_number'].isin(units)]

        # add unit numbers back to RUL prediction
        rul_df = pd.DataFrame(
                            {"unit_number": units,
                            "RUL": list(predictions_df.RUL)})

        # combine aircraft data with RUL predictions
        merged_df = pd.merge(aircraft_df, rul_df, left_on='unit_number', right_on='unit_number')

        # apply radio button filter
        if filter == "Yes":
            filtered_df = merged_df[merged_df.RUL <= threshold]
            st.dataframe(filtered_df)
        else:
            st.dataframe(merged_df)

        
 