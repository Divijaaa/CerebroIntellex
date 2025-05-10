import logging
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
from fastai.learner import load_learner
import pathlib

# Fix for Windows (PosixPath issue)
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath  

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Load MRI classification model
logger.info("Loading MRI classification model...")
try:
    model_path = r"C:\Users\Divija agrawal\OneDrive\Desktop\CerebroIntellex\models\regnet_model.pkl"
    model = load_learner(model_path)
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Error loading model: {e}")

def preprocess_image(image_file):
    """Preprocesses the uploaded image for the FastAI model."""
    logger.info("Received image for processing")
    print("🔹 Received image for processing")  # Debugging print

    image = Image.open(io.BytesIO(image_file))
    image = image.convert("RGB")  # Ensure 3 channels
    logger.info(f"Image mode: {image.mode}")

    return image  # FastAI handles resizing internally

@app.post("/classify-mri")
async def classify_mri(file: UploadFile = File(...)):
    """Handles MRI image classification."""
    logging.info("Received request at /classify-mri")
    try:
        image_data = await file.read()
        if not image_data:
            logging.error("Empty file received")
            return {"error": "No image data received"}

        logging.info(f"Processing file: {file.filename}")
        processed_image = preprocess_image(image_data)

        # Run inference
        pred_class, pred_idx, probs = model.predict(processed_image)
        
        # Convert probabilities tensor to list and round values
        rounded_probs = [round(float(p), 4) for p in probs]

        # Get confidence score for predicted class (rounded)
        confidence = round(float(probs[pred_idx]), 4)

        logging.info(f"Model prediction output: {pred_class}, Probabilities: {confidence}")

        return {
            "prediction": pred_class,
            "confidence": confidence
        }

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {"error": str(e)}
