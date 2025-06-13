# California Housing Price Prediction Deployment

## Overview
This project demonstrates how to deploy a machine learning model for California housing price prediction and make it accessible for use in PowerBI and other applications. The deployment pipeline includes model serialization, automated retraining, API serving, and containerization.

## Software and Tools Requirements

### 1. Model Serialization (Pickle)
Serialize (save) and load your trained model using the `pickle` library:
```python
import pickle
pickle.dump(regression, open('regmodel.pkl', 'wb'))
pickled_model = pickle.load(open('regmodel.pkl', 'rb'))
```

### 2. Apache Airflow: Automate Model Retraining
- Use Airflow to schedule and automate the retraining of your model.
- Place your Airflow DAG files in the `dags/` directory.

### 3. FastAPI: Build an API for Model Inference
- Provides endpoints for prediction and health checks:
    - `POST /predict`: Accepts JSON data for single or batch prediction.
    - `POST /predict_csv`: Accepts CSV file uploads for batch prediction.
    - `GET /`: Health check endpoint.
- Run the FastAPI app with:
    ```sh
    uvicorn app_fastapi:app --reload --host 0.0.0.0 --port 8000
    ```
    - `app_fastapi` is the Python file containing your FastAPI app.
    - `:app` refers to the FastAPI application object in that file.
    - The app will be accessible on port 8000 and open to external connections (e.g., from PowerBI).

### 4. Docker: Containerize the Application
- Create a `Dockerfile` to define how to build a container for your app.
- Build and run your Docker container:
    ```sh
    docker build -t my-fastapi-app .
    docker run -p 8000:8000 my-fastapi-app
    ```
    - The `-p 8000:8000` option maps port 8000 on your local machine to port 8000 in the container, making the API accessible at `http://localhost:8000`.
- Run Docker Desktop
    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

    wsl --install --no-distribution

---

**With this setup, you can automate retraining, serve predictions via API, and deploy your solution anywhere using Docker.**
