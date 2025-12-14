"""
Simple validation script for ML models.
Checks that models exist and can make predictions.
"""
import joblib
import os
import numpy as np


def test_model_files_exist():
    """Check that model files exist after training."""
    assert os.path.exists("models/model_v1.0.0.pkl"), "Model v1.0.0 not found"
    assert os.path.exists("models/model_v1.1.0.pkl"), "Model v1.1.0 not found"
    print("✓ Model files exist")


def test_model_can_predict():
    """Check that models can make predictions."""
    # Test v1.0.0
    model_v1 = joblib.load("models/model_v1.0.0.pkl")
    test_input = np.array([[1.0, 2.0, 3.0]])
    prediction = model_v1.predict(test_input)
    print(f"✓ Model v1.0.0 prediction: {prediction[0]:.2f}")

    # Test v1.1.0
    model_v2 = joblib.load("models/model_v1.1.0.pkl")
    prediction2 = model_v2.predict(test_input)
    print(f"✓ Model v1.1.0 prediction: {prediction2[0]:.2f}")


def test_model_coefficients():
    """Check that model has learned coefficients."""
    model = joblib.load("models/model_v1.0.0.pkl")
    print(f"✓ Model coefficients: {model.coef_}")


if __name__ == "__main__":
    print("Running model tests...")
    test_model_files_exist()
    test_model_can_predict()
    test_model_coefficients()
    print("\n✅ All tests passed!")
