from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

def retrain_model():
    # Load retrain features and target
    X_retrain = pd.read_csv('data/retrain_data.csv')
    y_retrain = pd.read_csv('data/retrain_target.csv').squeeze()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_retrain)
    model = LinearRegression()
    model.fit(X_scaled, y_retrain)
    pickle.dump(model, open('regmodel.pkl', 'wb'))
    pickle.dump(scaler, open('scaling.pkl', 'wb'))
    print("Retraining complete. Model and scaler saved.")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='retrain_linear_regression_model',
    default_args=default_args,
    schedule_interval='@weekly',  # Change as needed
    catchup=False,
) as dag:

    retrain_task = PythonOperator(
        task_id='retrain_model',
        python_callable=retrain_model,
    )
