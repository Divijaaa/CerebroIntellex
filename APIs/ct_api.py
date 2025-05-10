import logging
import io
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import numpy as np
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware


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
# Load model
logger.info("Loading model...")
try:
    model = tf.keras.models.load_model(r"C:\Users\Divija agrawal\OneDrive\Desktop\CerebroIntellex\models\CnnCTImage97.h5")
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Error loading model: {e}")

def preprocess_image(image_file):
    logger.info("Received image for processing")
    print("🔹 Received image for processing")  # Print to ensure visibility

    image = Image.open(io.BytesIO(image_file))
    image = image.resize((128, 128))
    image = image.convert("RGB")
    image_array = np.array(image) / 255.0

    logger.info(f"Image shape: {image_array.shape}")
    print(f"🔹 Image shape: {image_array.shape}")  # Print to ensure visibility

    image_array = np.expand_dims(image_array, axis=0)
    return image_array
@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    logging.info("Received request at /classify")
    try:
        image_data = await file.read()
        if not image_data:
            logging.error("Empty file received")
            return {"error": "No image data received"}

        logging.info(f"Processing file: {file.filename}")
        processed_image = preprocess_image(image_data)

        prediction = model.predict(processed_image)
        logging.info(f"Model prediction output: {prediction}")

        # Get the raw probability from the model (probability for "Ischemic Stroke")
        prob_ischemic = float(prediction[0][0])
        
        # Decide the predicted class and adjust confidence accordingly
        if prob_ischemic > 0.5:
            predicted_class = "Ischemic Stroke"
            final_confidence = prob_ischemic
        else:
            predicted_class = "Haemorrhagic Stroke"
            final_confidence = 1 - prob_ischemic

        logging.info(f"Predicted: {predicted_class}, Confidence: {final_confidence}")

        return {"prediction": predicted_class, "confidence": final_confidence}

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {"error": str(e)}
