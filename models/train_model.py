import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib


def train_model():

    # Load dataset
    df = pd.read_csv("hydraulic_system_dataset.csv")

    # Features and target
    X = df[["wind_speed", "turbulence", "route_risk"]]
    y = df["failure"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    # Model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluation
    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("\nReport:\n", classification_report(y_test, y_pred))

    # Save model
    joblib.dump(model, "hydraulic_failure_model.pkl")

    print("\nModel saved as hydraulic_failure_model.pkl")


if __name__ == "__main__":
    train_model()