"""
FastAPI ML Service with health and predict endpoints.
Supports model versioning through MODEL_VERSION environment variable.
"""
import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ML Model Service",
    description="ML deployment service with health and prediction endpoints",
    version="1.0.0"
)

# Get model version from environment
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")
MODEL_PATH = f"models/model_{MODEL_VERSION}.pkl"

# Load model at startup
model = None

@app.on_event("startup")
async def load_model():
    """Load the ML model on application startup."""
    global model
    try:
        model = joblib.load(MODEL_PATH)
        logger.info(f"Model {MODEL_VERSION} loaded successfully from {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Failed to load model from {MODEL_PATH}: {str(e)}")
        raise RuntimeError(f"Model loading failed: {str(e)}")


# Request/Response models
class PredictRequest(BaseModel):
    """Request model for prediction endpoint."""
    features: List[float] = Field(
        ...,
        description="List of feature values for prediction",
        example=[1.0, 2.0, 3.0]
    )

    class Config:
        # Support both 'x' and 'features' field names for backward compatibility
        populate_by_name = True


class PredictResponse(BaseModel):
    """Response model for prediction endpoint."""
    prediction: float
    model_version: str


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    version: str
    model_loaded: bool


# API Endpoints
@app.get("/health", response_model=HealthResponse)
async def health():
    """
    Health check endpoint.
    Returns service status and model version.
    """
    return {
        "status": "ok",
        "version": MODEL_VERSION,
        "model_loaded": model is not None
    }


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Prediction endpoint.
    Accepts feature values and returns model prediction.
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Service unavailable."
        )

    try:
        # Convert input to numpy array
        features = np.array([request.features])

        # Validate input shape (model expects 3 features)
        if features.shape[1] != 3:
            raise HTTPException(
                status_code=400,
                detail=f"Expected 3 features, got {features.shape[1]}"
            )

        # Make prediction
        prediction = model.predict(features)[0]

        logger.info(f"Prediction made: {prediction} for input: {request.features}")

        return {
            "prediction": float(prediction),
            "model_version": MODEL_VERSION
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "ML Model Deployment Service",
        "version": MODEL_VERSION,
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
