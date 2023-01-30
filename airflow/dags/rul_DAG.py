from airflow import DAG
#from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.sensors.file_sensor import FileSensor

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

    # check training data exists
    t1 = BashOperator(
        task_id='check_train_exists',
        depends_on_past = False, 
        bash_command='shasum /Users/dinushdealwis/Documents/ML_Projects/RUL/data/raw/train_FD001.txt',
        retries = 2,
        retry_delay = timedelta(seconds=15)
    )

    # check test feature data exists
    t2 = BashOperator(
        task_id='check_test_features',
        depends_on_past = False, 
        bash_command='shasum /Users/dinushdealwis/Documents/ML_Projects/RUL/data/raw/test_FD001.txt',
        retries = 2,
        retry_delay = timedelta(seconds=15)
    )

    # check test feature data exists
    t3 = BashOperator(
        task_id='check_test_labels',
        depends_on_past = False, 
        bash_command='shasum /Users/dinushdealwis/Documents/ML_Projects/RUL/data/raw/RUL_FD001.txt',
        retries = 2,
        retry_delay = timedelta(seconds=15)
    )

    [t1,t2,t3]


