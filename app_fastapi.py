from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

app = FastAPI()

# Load model and scaler at startup
with open('regmodel.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaling.pkl', 'rb') as f:
    scaler = pickle.load(f)

class PredictRequest(BaseModel):
    data: list

@app.post("/predict")
def predict(request: PredictRequest):
    # Expecting a list of lists (2D array)
    arr = np.array(request.data)
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    arr_scaled = scaler.transform(arr)
    prediction = model.predict(arr_scaled)
    return {"prediction": prediction.tolist()}

@app.post("/predict_csv")
def predict_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    arr_scaled = scaler.transform(df.values)
    prediction = model.predict(arr_scaled)
    return {"prediction": prediction.tolist()}

@app.get("/")
def root():
    return {"message": "Linear Regression Model API is running."}
