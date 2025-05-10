from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
import io
from PIL import Image, ImageFilter
import uvicorn
from fastapi.responses import StreamingResponse
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:5501",  # Your frontend URL
    "http://localhost:5501"  # Optional: Allow localhost as well
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def segment_hemorrhagic(image):
    mask = cv2.threshold(image, 250, 255, cv2.THRESH_BINARY)[1][:, :, 0]
    dst = cv2.inpaint(image, mask, 7, cv2.INPAINT_NS)
    dst = cv2.bitwise_not(dst)

    im1 = Image.fromarray(dst).filter(ImageFilter.MedianFilter(size=3))
    img_bright = cv2.convertScaleAbs(np.asarray(im1), alpha=1.8, beta=20)

    kernel = np.ones((3, 3), np.uint8)
    img_errode = cv2.dilate(img_bright, kernel)

    adjusted = adjust_gamma(img_errode, gamma=0.1)
    
    return adjusted

def segment_ischemic(image):
    mask = cv2.threshold(image, 250, 255, cv2.THRESH_BINARY)[1][:, :, 0]
    dst = cv2.inpaint(image, mask, 7, cv2.INPAINT_NS)

    im1 = Image.fromarray(dst).filter(ImageFilter.MedianFilter(size=3))
    img_bright = cv2.convertScaleAbs(np.asarray(im1), alpha=1.5, beta=10)

    kernel = np.ones((1, 1), np.uint8)
    img_errode = cv2.erode(img_bright, kernel)

    adjusted = adjust_gamma(img_errode, gamma=0.1)

    return adjusted

@app.post("/segment/")
async def segment_image(file: UploadFile = File(...), stroke_type: str = "ischemic"):
    # Read image
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Apply segmentation
    if stroke_type == "hemorrhagic":
        segmented_image = segment_hemorrhagic(image)
    else:
        segmented_image = segment_ischemic(image)

    # Convert to bytes
    _, img_encoded = cv2.imencode('.png', segmented_image)
    img_bytes = BytesIO(img_encoded.tobytes())
    return StreamingResponse(img_bytes, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8004)
# To run the FastAPI server, use the command:   uvicorn segmentation-api:app --reload