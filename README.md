# 🧠 CerebroIntellex: Stroke Prediction, Classification, and Segmentation Suite

**CerebroIntellex** is an end-to-end deep learning-based system designed for stroke analysis using CT and MRI scans. It integrates stroke **prediction**, **CT/MRI-based classification**, and **lesion segmentation**, all within an accessible, modular interface supported by pretrained models and APIs.

---

## 📌 Key Features

- 🔬 **CT & MRI Stroke Classification**  
  Classifies ischemic,hemorrhagic stroke and normal MRI and CT scan images using CNN-based models trained on medical imaging datasets.

- 🧠 **MRI Lesion Segmentation**  
  Uses Python scripts to segment ischemic and hemorrhagic regions from MRI scans for enhanced clinical insight.

- 🩺 **Stroke Prediction**  
  Machine learning models predict stroke probability using structured data inputs (age, hypertension, glucose, etc.).

- 🌐 **Modular Web Interface**  
  Built with HTML/CSS/JS for easy file upload, prediction viewing, and result interpretation.

- ⚙️ **RESTful APIs**  
  CT, MRI, segmentation, and prediction APIs (`APIs/`) for backend processing and model inference.


📊 Run Jupyter Notebooks

Open notebooks under Model_code/Classification/, Segmentation/, or Prediction/ to train or evaluate models.

🎯 Pretrained Models

models/CnnCTImage97.h5: CNN model trained on CT scans (97% accuracy)

models/stroke_prediction_model.joblib: Structured data ML model

models/regnet_model.pkl: MRI classification model



