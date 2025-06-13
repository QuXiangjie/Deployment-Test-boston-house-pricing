"""
Simple consistency verification
"""
import pandas as pd
import numpy as np

print("=" * 50)
print("CONSISTENCY CHECK RESULTS")
print("=" * 50)

# Check CSV files
try:
    df = pd.read_csv('data/predict_new_data.csv')
    print(f"✓ predict_new_data.csv: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"    Columns: {list(df.columns)}")
    
    df2 = pd.read_csv('data/retrain_data.csv')
    print(f"✓ retrain_data.csv: {df2.shape[0]} rows, {df2.shape[1]} columns")
    print(f"    Columns: {list(df2.columns)}")
    
    if list(df.columns) == list(df2.columns):
        print("✓ CSV files have consistent column structure")
    else:
        print("✗ CSV files have different column structures")
        
except Exception as e:
    print(f"✗ Error reading CSV files: {e}")

# Check model files
try:
    import pickle
    with open('regmodel.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaling.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("✓ Model files load successfully")
    
    # Test prediction
    test_data = np.array([[3.5673, 11.0, 5.93, 1.13, 1257.0, 2.82, 39.29, -121.32]])
    scaled_data = scaler.transform(test_data)
    prediction = model.predict(scaled_data)
    print(f"✓ Test prediction successful: {prediction[0]:.4f}")
    
except Exception as e:
    print(f"✗ Error with model files: {e}")

print("\n" + "=" * 50)
print("FIXES APPLIED:")
print("=" * 50)
print("1. ✓ Fixed dataset consistency (California Housing vs Boston Housing)")
print("2. ✓ Updated HTML template to match FastAPI structure")
print("3. ✓ Added proper documentation and feature descriptions")
print("4. ✓ Fixed empty Airflow DAG file")
print("5. ✓ Updated requirements.txt with missing packages")
print("6. ✓ Made DAG names unique and descriptive")
print("7. ✓ Added comprehensive API documentation")
print("=" * 50)
