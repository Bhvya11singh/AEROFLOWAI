from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

# Load trained model
model = joblib.load("hydraulic_failure_model.pkl")


@app.get("/")
def home():
    return {"message": "Hydraulic Failure Prediction API is running"}


@app.post("/predict")
def predict_failure(wind_speed: float, turbulence: float, route_risk: float):

    input_data = np.array([[wind_speed, turbulence, route_risk]])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    return {
        "failure_prediction": int(prediction),
        "failure_probability": float(probability)
    }