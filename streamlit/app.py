import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from src.data.preprocess import feature_engineering, feature_selection, make_prediction
from pathlib import Path
import streamlit as st
from PIL import Image
import pandas as pd
from random import choice
from bulk_upload_page import bulk_upload
from single_predict_page import single_predict
from explore_page import explore
import streamlit.components.v1 as components
st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    
    # title, subtitle
    st.markdown("""---""")
    st.title("Predicting Remaining Useful Life")
    st.subheader("ML Approach for Turbofan Engine Maintenance")
    st.markdown("""---""")
    
    # set pages
    page = st.sidebar.selectbox("Choose prediction method", ("Explore Data", "Bulk Predictions", "RUL simulator"))

    # User selects bulk upload option
    if page == "Explore Data":
        explore()

    if page == "Bulk Predictions":
        bulk_upload()

    if page == "RUL simulator":
        single_predict()





if __name__ == '__main__':
    main()






