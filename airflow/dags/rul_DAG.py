import os, sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from src.data.training import training
from airflow import DAG
#from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from pathlib import Path

# docker-airflow-master % docker-compose -f docker-compose-LocalExecutor.yml up -d

# instantiate DAG
with DAG(
    'rul-flow',
    default_args={
        'owner': 'Dinush De Alwis', 
        'depends_on_past': False,
        'email': ['dinushdealwis@gmail.com'], 
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
        },
    description='Predicting Remaining Useful Life of Turbofan Engines',
    schedule_interval='@daily',
    catchup=False,
    start_date=datetime(2023, 1, 8)
) as dag:

    def check_file():
        path = Path(__file__).parent.parent.parent.parent.resolve() 
        filename = 'data/raw/train_FD001.txt'
        fullpath = path.joinpath(filename)
        file_path = fullpath
        if os.path.isfile(file_path):
            print(f"File {file_path} exists!")
        else:
            print(f"File {file_path} does not exist.")

    t1 = PythonOperator(
        task_id='check_file_task',
        python_callable=check_file,
        dag=dag)
    

    def training():
        training


    t2 = PythonOperator(
        task_id = 'run_training',
        python_callable = training,
        dag=dag
    )


    t1 >> t2





