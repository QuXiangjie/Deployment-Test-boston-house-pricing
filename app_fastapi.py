from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import os
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="California Housing Price Prediction API", 
              description="API for predicting California housing prices using Linear Regression")

# Load model and scaler at startup
with open('regmodel.pkl', 'rb') as f:
    model = pickle.load(f)
with open('scaling.pkl', 'rb') as f:
    scaler = pickle.load(f)

class PredictRequest(BaseModel):
    data: list
    
    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    [3.5673, 11.0, 5.93, 1.13, 1257.0, 2.82, 39.29, -121.32]
                ]
            }
        }

@app.get("/", response_class=HTMLResponse)
def root():
    """Serve the API documentation page."""
    # Read the HTML template
    html_path = os.path.join("templates", "home.html")
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return """
        <html>
            <head><title>California Housing Price Prediction API</title></head>
            <body>
                <h1>California Housing Price Prediction API</h1>
                <p>API endpoints:</p>
                <ul>
                    <li>GET / - This documentation page</li>
                    <li>POST /predict - Predict with JSON data</li>
                    <li>POST /predict_csv - Predict with CSV file upload</li>
                    <li>GET /docs - Interactive API documentation</li>
                </ul>
            </body>
        </html>
        """

@app.post("/predict")
def predict(request: PredictRequest):
    """
    Predict housing prices using the trained model.
    
    Expected features (in order):
    1. MedInc - Median income in block group
    2. HouseAge - Median house age in block group  
    3. AveRooms - Average number of rooms per household
    4. AveBedrms - Average number of bedrooms per household
    5. Population - Block group population
    6. AveOccup - Average number of household members
    7. Latitude - Block group latitude
    8. Longitude - Block group longitude
    """
    # Expecting a list of lists (2D array)
    arr = np.array(request.data)
    if arr.ndim == 1:
        # number of rows = 1, number of columns = number of features
        arr = arr.reshape(1, -1)
    
    # Validate input dimensions
    if arr.shape[1] != 8:
        return {"error": f"Expected 8 features, got {arr.shape[1]}"}
    
    arr_scaled = scaler.transform(arr)
    prediction = model.predict(arr_scaled)
    return {
        "prediction": prediction.tolist(),
        "input_shape": arr.shape,
        "model_info": "California Housing Price Prediction (Linear Regression)"
    }

@app.post("/predict_csv")
def predict_csv(file: UploadFile = File(...)):
    """
    Predict housing prices from a CSV file upload.
    
    CSV should contain columns: MedInc,HouseAge,AveRooms,AveBedrms,Population,AveOccup,Latitude,Longitude
    """
    df = pd.read_csv(file.file)
    
    # Validate CSV structure
    expected_columns = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
    if not all(col in df.columns for col in expected_columns):
        return {"error": f"CSV must contain columns: {expected_columns}"}
    
    # Select only the required columns in correct order
    df = df[expected_columns]
    
    arr_scaled = scaler.transform(df.values)
    prediction = model.predict(arr_scaled)
    return {
        "prediction": prediction.tolist(),
        "input_shape": df.shape,
        "model_info": "California Housing Price Prediction (Linear Regression)"
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "api_version": "0.0.1"
    }

@app.get("/test", response_class=HTMLResponse)
def test_page():
    """Serve the interactive API test page."""
    html_path = os.path.join("templates", "api_test.html")
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return """
        <html>
            <head><title>Test Page Not Found</title></head>
            <body>
                <h1>API Test Page Not Found</h1>
                <p>The test page template is missing.</p>
                <p><a href="/docs">Go to API Documentation</a></p>
            </body>
        </html>
        """

@app.get("/favicon.ico")
def favicon():
    """Handle favicon requests to avoid 404 errors."""
    return {"message": "No favicon available"}






class PowerBIRequest(BaseModel):
    """Power BI specific request format"""
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float
    
class BulkPredictionRequest(BaseModel):
    """For bulk predictions from Power BI datasets"""
    records: List[PowerBIRequest]

@app.post("/powerbi/predict")
def powerbi_predict(request: PowerBIRequest):
    """
    Power BI friendly single prediction endpoint
    """
    try:
        # Convert to array format
        features = [[
            request.MedInc, request.HouseAge, request.AveRooms, request.AveBedrms,
            request.Population, request.AveOccup, request.Latitude, request.Longitude
        ]]
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        
        # Convert to actual price
        predicted_price = prediction * 100000
        
        # Categorize price
        if predicted_price < 200000:
            price_category = "Low"
        elif predicted_price < 400000:
            price_category = "Medium"
        else:
            price_category = "High"
        
        return {
            "MedInc": request.MedInc,
            "HouseAge": request.HouseAge,
            "AveRooms": request.AveRooms,
            "AveBedrms": request.AveBedrms,
            "Population": request.Population,
            "AveOccup": request.AveOccup,
            "Latitude": request.Latitude,
            "Longitude": request.Longitude,
            "PredictedPrice": round(predicted_price, 2),
            "PriceCategory": price_category,
            "PredictionDate": datetime.now().isoformat(),
            "ModelVersion": "v1.0"
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/powerbi/bulk-predict")
def powerbi_bulk_predict(request: BulkPredictionRequest):
    """
    Bulk prediction for Power BI datasets
    """
    try:
        results = []
        
        for record in request.records:
            # Convert to array format
            features = [[
                record.MedInc, record.HouseAge, record.AveRooms, record.AveBedrms,
                record.Population, record.AveOccup, record.Latitude, record.Longitude
            ]]
            
            # Scale and predict
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled)[0]
            predicted_price = prediction * 100000
            
            # Categorize price
            if predicted_price < 200000:
                price_category = "Low"
            elif predicted_price < 400000:
                price_category = "Medium"
            else:
                price_category = "High"
            
            result = {
                "MedInc": record.MedInc,
                "HouseAge": record.HouseAge,
                "AveRooms": record.AveRooms,
                "AveBedrms": record.AveBedrms,
                "Population": record.Population,
                "AveOccup": record.AveOccup,
                "Latitude": record.Latitude,
                "Longitude": record.Longitude,
                "PredictedPrice": round(predicted_price, 2),
                "PriceCategory": price_category
            }
            results.append(result)
        
        return {"predictions": results, "count": len(results)}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/powerbi/sample-data")
def get_powerbi_sample():
    """
    Generate sample data for Power BI testing
    """
    import random
    
    samples = []
    for i in range(100):  # Generate 100 sample records
        record = {
            "ID": i + 1,
            "MedInc": round(random.uniform(1, 15), 4),
            "HouseAge": random.randint(1, 52),
            "AveRooms": round(random.uniform(3, 10), 2),
            "AveBedrms": round(random.uniform(0.8, 2.0), 2),
            "Population": random.randint(500, 5000),
            "AveOccup": round(random.uniform(2, 6), 2),
            "Latitude": round(random.uniform(32, 42), 2),
            "Longitude": round(random.uniform(-125, -114), 2)
        }
        samples.append(record)
    
    return {"data": samples}

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app_fastapi:app", host="0.0.0.0", port=port)
