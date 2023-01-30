## **Predicting Remaining Useful Life (RUL) of Turbofan Engines: A Machine Learning Approach**

#### Project Description:
---------------------
The U.S. DoD’s Joint Artificial Intelligence Center has designated Predictive Maintenance as one of its two founding National Mission Initiatives (NMIs). The challenge we are trying to solve is accurately predicting the remaining useful life (RUL) of turbofan engines measured in operations cycles. RUL is equivalent of number of flights remaining for the engine.

Turbofans are widely used in aircraft propulsion, such aircrafts include military fighter jets. Accurate predictive maintenance of turbofan useful remaining life has huge potential to drastically reduce costs, increase mission readiness and even save lives of service members. 

- Cost reductions can come in the form of to better inventory and cash-flow management 
- Troop morale could be better knowing they are using aircrafts with reduced probability of failure
- With lower probability of potentially failing turbo engines in the field, critical missions could be executed with increased chances of success

#### Project Aim and Key Deliverables:
---------------------

The aim of this project is to build a reproducible machine learning model and data pipeline that allows for the DoD's Joint Artifiicial Intelligence Center to accurately predict RUL, experiment with new models and improve their overall RUL prediction capability. 

Key Deliverables:

- detailed documentation of data pipelines, data lineage, model experimentation, exploratory data analysis and data preprocessing 
- a final model that can be called by a front-end application for real time RUL prediction
- a Streamlit front-end app that monitors, simulates and predicts RUL for a given set of sensor readings


#### Data:
---------------------
In terms of data sources, we will be using the NASA turbofan engine degradation datasets. These can be sourced directly from NASA’s Intelligence Systems Division https://www.nasa.gov/intelligent-systems-division#turbofan or from Kaggle https://www.kaggle.com/datasets/behrad3d/nasa-cmaps


#### Directory Structure
---------------------

    .
    ├── AUTHORS.md
    ├── LICENSE
    ├── README.md
    ├── models  <- compiled model .pkl or HDFS or .pb format
    ├── config  <- any configuration files
    ├── data
    │   ├── interim <- data in intermediate processing stage
    │   ├── processed <- data after all preprocessing has been done
    │   └── raw <- original unmodified data acting as source of truth and provenance
    ├── docs  <- usage documentation or reference papers
    ├── notebooks <- jupyter notebooks for exploratory analysis and explanation 
    ├── reports <- generated project artefacts eg. visualisations or tables
    │   └── figures
    └── src
        ├── data-proc <- scripts for processing data eg. transformations, dataset merges etc. 
        ├── viz  <- scripts for visualisation during EDA, modelling, error analysis etc. 
        ├── modeling    <- scripts for generating models
    |--- environment.yml <- file with libraries and library versions for recreating the analysis environment
   
#### How to use
---------------------

To reproduce the results end-to-end...

To simply run the front end Streamlit application...

