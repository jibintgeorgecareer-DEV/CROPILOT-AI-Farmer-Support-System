🌱 Cropilot-AI

### Smarter Soil, Healthier Crops, Expert Support

Cropilot is an AI-powered agriculture web application developed to help farmers with crop disease detection, soil recommendations, market price insights, and agriculture officer support and CHATBOT system.

The system uses Deep Learning and Image Classification techniques to identify crop diseases from uploaded images and provide treatment suggestions, symptoms, and impact analysis.

---

# 🤖 AI Disease Detection (Main Part)

Cropilot currently supports:

* Cocoa disease detection
* Potato disease detection
* Tomato disease detection

There are two models (cocoa_disease.h5 & potato_tomato.h5) trained on my laptop with tensorflow & Keras.
The image datasets are from Kaggle.

The system uses:

* tensorflow : for tarining the model on kaggle image datasets
* Keras : high‑level API on top of TensorFlow
* MobileNetV2 : CNN model for image classification by transfer training


Farmers can upload crop images, and the trained AI model predicts the disease with confidence score, symptoms, impact, and treatment recommendations.

---

# 🚀 Features

* ✅ AI-powered crop disease detection
* ✅ Smart soil recommendation system
* ✅ Agriculture officer connectivity
* ✅ Farmer dashboard and profile management
* ✅ Crop and disease report management
* ✅ Market price checking
* ✅ AI chatbot for basic farming questions
* ✅ friendly UI/UX

---

# 🛠️ Tech Stack

| Layer           | Technologies Used                |
| --------------- | -------------------------------- |
| Backend         | Python, Django                   |
| Frontend        | HTML, CSS, Bootstrap, JavaScript |
| Database        | SQLite                           |
| AI/ML           | TensorFlow, Keras, MobileNetV2   |
| Version Control | Git & GitHub                     |


# 📂 Project Structure

```text
CROPPILOT_FULL_PROJECT/
│── croppilot_app/       # Main Django application
    ml_models/           # Trained AI models (.h5)
    ml_function/         # training functions, chatbot engine, model loading
│── croppilot_project/  
    static/              # CSS, JS, Images
│── templates/           # HTML templates        
│── media/               # Uploaded crop images
│── manage.py            # Django entry point

```

---

# 🌾 How Cropilot Works

1. Farmer uploads crop image
2. AI model analyzes the image
3. Disease is predicted
4. Confidence score is generated
5. Symptoms, impact, and treatment are displayed
6. Reports are saved in farmer dashboard

---

# 🔮 Future Improvements

* Add more crop disease datasets
* Support coconut, rice, banana, pepper, and cardamom diseases
* Improve AI model accuracy
* Local language support
* Crop Management Guide for Young Farmers
* Add multilingual chatbot support
* Real-time weather integration
* Mobile application support

---
⚙️ Installation 

The frameworks tensorflow and keras not supported for python 3.14 ,So i created virtual environment for 
python 3.10 with venv
---

# 👨‍💻 Developed By

**Jibin T George**
Final Year BCA Project (6 th semester)

---
