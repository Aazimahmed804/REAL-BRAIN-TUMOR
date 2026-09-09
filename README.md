# BRAIN TUMOR DETECTION APP
Brain Tumor Detection — Deep Learning Web App

A full-stack machine learning web application that detects and classifies brain tumors from MRI scans using a CNN (VGG16-based) model, wrapped in a Flask web app with user authentication, prediction history, and cloud deployment.

Live Demo: real-brain-tumor-zpw0o.faable.link
GitHub Repo: [github.com/Aazimahmed804/REAL-BRAIN-TUMOR](https://www.google.com/search?q=https%3A%2F%2Fgithub.com%2FAazimahmed804%2FREAL-BRAIN-TUMOR)
Model Weights (Hugging Face): huggingface.co/aazim12/model.h5

---

Overview

This project takes an MRI brain scan image as input and classifies it into one of four categories:

* Glioma
* Meningioma
* Pituitary Tumor
* No Tumor

The model uses transfer learning on VGG16 — pretrained ImageNet weights as a feature extractor, with a custom classification head trained on labeled MRI scan data — served through a Flask backend with a SQLite database for user accounts and prediction history.

---

Features

* User registration and session-based login
* MRI image upload and real-time prediction
* Confidence score for each prediction
* Prediction history per user, stored in a database
* Fully deployed on the cloud (Faable), with the trained model served externally via Hugging Face due to file-size constraints on GitHub

---

Tech Stack

* Backend: Flask, Flask-SQLAlchemy, Flask-WTF
* ML / Deep Learning: TensorFlow, Keras (VGG16 + Transfer Learning)
* Image Processing: Pillow, NumPy
* Database: SQLite
* Model Hosting: Hugging Face Hub
* Deployment: Faable (Git-based cloud deployment)
* Server: Gunicorn

---

Architecture

User uploads MRI image
↓
Flask receives file → saves to /uploads
↓
Image preprocessed (resize, normalize) via Keras utils
↓
Transfer-learned VGG16 model predicts tumor class + confidence
↓
Result + confidence saved to SQLite (Prediction table)
↓
Rendered back to user

The trained model (model.h5, ~150MB) exceeds GitHub's 100MB file-size limit for direct commits. To solve this without Git LFS overhead, the app downloads the model from Hugging Face Hub at container startup if it isn't already present locally — keeping the Git repository lightweight while still serving the full model in production.

---

The Debugging Journey

Shipping this from "works on my machine" to a live, public URL surfaced a series of real-world deployment problems — each one a genuine learning point:

1. FileNotFoundError on the model file at boot — the working directory in production didn't match local assumptions, and the model wasn't even present on the server.
2. 152MB model vs. GitHub's 100MB push limit — solved by hosting the model on Hugging Face Hub and downloading it programmatically at app startup instead of committing it to Git.
3. no such table: user (SQLAlchemy OperationalError) — db.create_all() was only called inside an if **name** == "**main**": block, which never executes under Gunicorn. Fixed by moving table creation to module load time via app.app_context().
4. Missing dependencies in production (email_validator, Pillow) — packages that worked locally (already installed system-wide) but weren't declared in requirements.txt, causing ImportErrors only in the clean production environment.

Each of these is a classic "it works locally but breaks in production" class of bug — the kind of debugging experience that only comes from actually shipping a project end-to-end.

---

Running Locally

git clone [https://github.com/Aazimahmed804/REAL-BRAIN-TUMOR.git](https://github.com/Aazimahmed804/REAL-BRAIN-TUMOR.git)
cd REAL-BRAIN-TUMOR
pip install -r requirements.txt
python app.py

The app will download model.h5 from Hugging Face automatically on first run if it isn't already in models/.

---

Future Improvements

* Add Docker support for consistent environments across local dev and production
* Move from SQLite to PostgreSQL for production-grade persistence
* Add model evaluation metrics (precision/recall per class) to the README
* Add automated tests and CI/CD pipeline

---

Acknowledgements

Built and debugged end-to-end — from model training to a live cloud deployment — as a hands-on learning project in applied machine learning and MLOps fundamentals.
