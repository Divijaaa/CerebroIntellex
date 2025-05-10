# 🧠 CerebroIntellex

**CerebroIntellex** is an AI-powered stroke analysis system that integrates **clinical data**, **CT & MRI image classification**, and **MRI image segmentation** to assist in early detection and understanding of brain strokes.

---

## 🚀 Key Features

- ✅ Predict stroke risk from clinical features.
- ✅ Classify **CT and MRI brain scans** into:
  - `Normal`
  - `Ischemic`
  - `Hemorrhagic`
- ✅ Segment stroke-affected areas in MRI scans.
- ✅ RESTful API integration via **FastAPI**.

---

## 🧠 Core Modules

| Module | Task | Model | Classes | Framework |
|--------|------|-------|---------|-----------|
| `stroke_prediction_model/` | Stroke prediction (tabular) | LDA | Stroke / No stroke | scikit-learn |
| `CNNCTImage97/` | CT classification | Custom CNN | Ischemic, Hemorrhagic | CNN |
| `regnet_model/` | MRI classification | CNN (RegNet) | Normal, Ischemic, Hemorrhagic | PyTorch |
| `mri_segmentation/` | MRI segmentation | Python functions (custom) | Pixel-wise masks | Python |
| `APIs/` | REST API | FastAPI | - | Python / Uvicorn |

---

## ⚙️ Installation

```bash
git clone https://github.com/Divijaaa/CerebroIntellex.git
cd CerebroIntellex
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
---
## 🌐 Running the API
After completing the installation, you can start the FastAPI server to expose the API endpoints.

1. Navigate to the APIs/ directory:
   ```bash
   cd APIs
   ```
2. Run the FastAPI server with Uvicorn:
   ```bash
   uvicorn <api_name>:app --reload --port <port_no>
   ```
   This will start the FastAPI server with live reloading.
3. Access API Documentation:
   FastAPI automatically generates an interactive documentation for the API. You can access it at:
   Swagger UI: http://localhost:<port_number>/docs
   ReDoc: http://localhost:<port_number>/redoc
   You can test all available endpoints directly from these documentation interfaces.
---
## 🧪 API Endpoints

| Endpoint        | Port | Method | Description                                                                                    |
| --------------- | ---- | ------ | ---------------------------------------------------------------------------------------------- |
| `/predict`      | 8080 | POST   | Accepts clinical data in JSON format to predict stroke risk.                                   |
| `/classify`     | 8001 | POST   | Classifies CT brain scans as **Ischemic** or **Hemorrhagic** (upload CT image).                |
| `/classify-mri` | 8003 | POST   | Classifies MRI brain scans as **Normal**, **Ischemic**, or **Hemorrhagic** (upload MRI image). |
| `/segment`      | 8004 | POST   | Segments MRI brain scan to highlight stroke-affected areas (upload MRI image).                 |

---

## 💡 Frontend Usage
To interact with the API via a simple web interface, use the HTML files provided in the pages/ directory.

### 📂 Pages Overview
- login/ – User login interface (static demo).
- prediction/ – Form to input clinical data for stroke risk prediction.
- prediction-results/ – Displays predicted stroke outcome.
- upload-image/ – Upload CT or MRI images for classification.
- results/ – Shows classification results (CT/MRI).
- segmentation/seg-results.html – Displays segmentation result on uploaded MRI.

### ▶️ To Launch Frontend:
You can open any of the HTML files in your browser directly. Make sure the corresponding API is running in the background. For example:

- For stroke prediction (prediction.html), ensure /predict API (port 8080) is running.
- For CT classification (upload-image.html), ensure /classify API (port 8001) is running.
- For MRI classification, ensure /classify-mri API (port 8003) is running.
- For segmentation results, ensure /segment API (port 8004) is running.

Note: Make sure to run the corresponding API server on each of the required ports (8080, 8001, 8003, 8004) for the frontend to work correctly. You can either start them in different terminal windows or configure them to run concurrently.

---
## 📁 Project Structure

```
CerebroIntellex/
├── APIs/                          # FastAPI-based REST APIs
│   ├── ct_api/
│   ├── mri_api/
│   ├── pred_api/
│   └── segmentation-api/
│
├── model_code/                   # Code for ML models
│   ├── Classification/
│   ├── Prediction/
│   └── Segmentation/
│
├── models/                       # Pretrained model files
│   ├── CnnCTImage97.h5
│   ├── regnet_model.pkl
│   └── stroke_prediction_model.joblib
│
├── pages/                        # Frontend HTML/CSS/JS files
│   ├── login/
│   ├── prediction/
│   ├── prediction-results/
│   ├── upload-image/
│   ├── results/
│   └── segmentation/
│
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```
---