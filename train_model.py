"""
Script to train a simple ML model for the deployment assignment.
Creates a linear regression model and saves it as a pickle file.
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import joblib
import os

def train_and_save_model(version="v1.0.0"):
    """Train a simple linear regression model and save it."""
    # Generate synthetic dataset
    X, y = make_regression(n_samples=1000, n_features=3, noise=10, random_state=42)

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)

    # Save model
    model_path = f"models/model_{version}.pkl"
    joblib.dump(model, model_path)

    print(f"Model trained and saved to {model_path}")
    print(f"Model score: {model.score(X, y):.4f}")
    print(f"Model coefficients: {model.coef_}")

    return model_path

if __name__ == "__main__":
    # Train v1.0.0
    train_and_save_model("v1.0.0")

    # Train v1.1.0 (slightly different random state for demonstration)
    X, y = make_regression(n_samples=1000, n_features=3, noise=10, random_state=43)
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, "models/model_v1.1.0.pkl")
    print("\nModel v1.1.0 trained and saved to models/model_v1.1.0.pkl")
    print(f"Model score: {model.score(X, y):.4f}")
