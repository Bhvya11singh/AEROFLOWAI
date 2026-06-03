import joblib
import numpy as np

# Load trained model
model = joblib.load("hydraulic_failure_model.pkl")

print("\n🚀 AEROFLOW AI FAILURE PREDICTION SYSTEM\n")

# User inputs
wind_speed = float(input("Enter wind speed: "))
turbulence = float(input("Enter turbulence level: "))
route_risk = float(input("Enter route risk score: "))

# Prepare input
input_data = np.array([[wind_speed, turbulence, route_risk]])

# Prediction
prediction = model.predict(input_data)[0]

# Probability
probability = model.predict_proba(input_data)[0][1]

print("\n==============================")
print("AI SYSTEM REPORT")
print("==============================")

print(f"Failure Probability: {probability:.2f}")

if probability < 0.3:
    print("SYSTEM STATUS: SAFE 🟢")

elif probability < 0.7:
    print("SYSTEM STATUS: WARNING 🟡")

else:
    print("SYSTEM STATUS: CRITICAL 🔴")

print("==============================")