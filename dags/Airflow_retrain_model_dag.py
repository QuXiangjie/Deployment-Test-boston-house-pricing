from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

def retrain_model():
    """
    Retrain the California Housing Price Prediction model
    """
    # Load retrain features and target
    X_retrain = pd.read_csv('data/retrain_data.csv')
    y_retrain = pd.read_csv('data/retrain_target.csv').squeeze()
    
    # Initialize and fit scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_retrain)
    
    # Initialize and fit model
    model = LinearRegression()
    model.fit(X_scaled, y_retrain)
    
    # Save model and scaler
    pickle.dump(model, open('regmodel.pkl', 'wb'))
    pickle.dump(scaler, open('scaling.pkl', 'wb'))
    
    print("Retraining complete. Model and scaler saved.")
    print(f"Model trained on {X_retrain.shape[0]} samples with {X_retrain.shape[1]} features")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='retrain_california_housing_model_v2',
    default_args=default_args,
    description='Retrain California Housing Price Prediction Model (Version 2)',
    schedule_interval='@weekly',  # Retrain weekly
    catchup=False,
) as dag:

    retrain_task = PythonOperator(
        task_id='retrain_model',
        python_callable=retrain_model,
    )
