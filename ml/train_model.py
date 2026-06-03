import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("hydraulic_system_dataset.csv")

# Features
X = df[["wind_speed", "turbulence", "route_risk"]]

# Target
y = df["failure"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestClassifier()

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("\n🚀 MODEL TRAINED SUCCESSFULLY")
print(f"Accuracy: {accuracy:.2f}")

# Save model
joblib.dump(model, "hydraulic_failure_model.pkl")

print("Model saved as hydraulic_failure_model.pkl")