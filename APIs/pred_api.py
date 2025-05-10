
from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

# Configure logging to print to the terminal
logging.basicConfig(
    level=logging.INFO,  # Set logging level to INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # Output logs to console
    ]
)

logger = logging.getLogger(__name__)

# Load the trained model
MODEL_PATH = r"C:\Users\Divija agrawal\OneDrive\Desktop\CerebroIntellex\models\stroke_prediction_model.joblib"
try:
    model = joblib.load(MODEL_PATH)
    logger.info("✅ Model loaded successfully.")
except FileNotFoundError:
    logger.error(f"❌ Model file not found at {MODEL_PATH}")
    raise RuntimeError("Model file not found. Ensure it's placed in the correct directory.")
except Exception as e:
    logger.error(f"❌ Failed to load model: {str(e)}")
    raise RuntimeError(f"Failed to load model: {str(e)}")

# Initialize FastAPI app
app = FastAPI()

# CORS Configuration
origins = [
    "http://127.0.0.1:5501",  # If using VSCode Live Server
    "http://localhost:8000",   # Localhost
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request body model
class StrokePredictionInput(BaseModel):
    age: float
    avg_glucose_level: float
    bmi: float
    hypertension: int
    heart_disease: int
    ever_married: str
    work_type: str
    Residence_type: str
    smoking_status: str

@app.post("/predict")
def predict_stroke(data: StrokePredictionInput):
    try:
        # Convert input to DataFrame
        input_data = pd.DataFrame([data.dict()])

        # Normalize categorical values consistently
        input_data["ever_married"] = input_data["ever_married"].str.strip().str.capitalize()  # Capitalize first letter
        input_data["work_type"] = input_data["work_type"].str.strip().str.replace(" ", "_").str.lower()  # Lowercase and replace space
        input_data["Residence_type"] = input_data["Residence_type"].str.strip().str.capitalize()  # Capitalize first letter
        input_data["smoking_status"] = input_data["smoking_status"].str.strip().str.replace(" ", "_").str.lower()  # Lowercase and replace space

        # Convert hypertension and heart_disease to 0 or 1 if they are 'yes'/'no'
        input_data["hypertension"] = input_data["hypertension"].apply(lambda x: 1 if x == 'yes' else 0)
        input_data["heart_disease"] = input_data["heart_disease"].apply(lambda x: 1 if x == 'yes' else 0)

        # Log the normalized input data
        logger.info(f"Received Normalized Input Data: {input_data}")

        # Make prediction
        prediction = model.predict(input_data)[0]
        probability = float(model.predict_proba(input_data)[0][1])

        # Map prediction to labels
        stroke_label = "stroke" if prediction == 1 else "no stroke"

        response = {
            "stroke_prediction": stroke_label,
            "stroke_probability": round(probability, 4)
        }

        # Log prediction result
        logger.info(f"Prediction: {response}")

        return response

    except Exception as e:
        logger.error(f"❌ Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")


