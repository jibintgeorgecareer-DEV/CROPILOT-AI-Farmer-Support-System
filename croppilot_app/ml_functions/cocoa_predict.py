import numpy as np
import tensorflow as tf
import time
from tensorflow.keras.preprocessing import image

# Load cocoa model once
model = tf.keras.models.load_model(
    "croppilot_app/ml_models/cocoa_disease_model.h5"
)

# Must match folder names used during training
class_names = [
    "black_pod_rot",
    "frosty_pod_rot",
    "healthy",
    "pod_borer",
    "witches_broom"
]

# Treatment suggestions
TREATMENTS = {

    "black_pod_rot":
    "Remove and destroy infected cocoa pods as soon as possible to stop the disease from spreading. "
    "Keep the farm clean, improve water drainage, and reduce excess shade to lower moisture levels. "
    "Spraying recommended fungicides such as Bordeaux mixture can help protect healthy pods.",

    "frosty_pod_rot":
    "Cut and remove diseased pods immediately before the fungus spreads to nearby pods. "
    "Prune overcrowded branches to improve airflow and sunlight inside the farm. "
    "Use suitable fungicides or biological controls like Trichoderma to reduce infection.",

    "healthy":
    "Your cocoa plant appears healthy and no treatment is currently needed. "
    "Continue regular watering, proper fertilizer use, pruning, and field monitoring to maintain healthy growth.",

    "pod_borer":
    "Harvest ripe pods regularly to reduce insect breeding. "
    "Remove damaged pods from the farm and keep the plantation clean. "
    "Pruning excess branches and reducing heavy shade can help lower pest attacks. "
    "Protective pod covers or safe insect control methods may also help.",

    "witches_broom":
    "Cut and destroy infected branches, shoots, and broom-like growths to stop the disease from spreading. "
    "Prune the cocoa trees regularly to keep them healthy and improve airflow. "
    "Using disease-resistant cocoa varieties and maintaining good farm hygiene can help reduce future infections.",

}

IMPACT = {

    "black_pod_rot":
    "This disease can destroy a large number of cocoa pods if not controlled early. "
    "It spreads quickly during rainy and humid weather and can greatly reduce cocoa yield and farmer income.",

    "frosty_pod_rot":
    "Frosty pod rot is a very serious cocoa disease that can spread rapidly across farms. "
    "In severe cases, most of the pods may become damaged, leading to heavy production loss and poor harvest quality.",

    "healthy":
    "No harmful disease impact detected on the plant. "
    "The cocoa plant appears healthy and capable of normal growth and production under proper care.",

    "pod_borer":
    "Pod borer insects damage the beans inside the cocoa pod, reducing both quality and quantity. "
    "If the attack becomes severe, farmers may experience major crop loss and lower market value for cocoa beans.",

    "witches_broom":
    "This disease weakens the cocoa tree over time and reduces pod production. "
    "Infected trees may produce fewer healthy pods, affecting long-term farm productivity and overall cocoa yield.",

}

SYMPTOMS = {

    "black_pod_rot":
    "Brown or black patches appear on cocoa pods and slowly spread across the surface. "
    "The pod starts rotting and may develop white fungal growth. "
    "Infected pods become weak, spoiled, and unsuitable for good bean production.",

    "frosty_pod_rot":
    "A white powder-like or frosty layer appears on the cocoa pod surface. "
    "The pod gradually becomes dry, damaged, and unhealthy. "
    "If not controlled early, the disease can spread quickly to nearby pods.",

    "healthy":
    "The cocoa plant looks healthy and no major disease symptoms are detected. "
    "Leaves, stems, and pods appear normal. "
    "Continue regular watering, fertilizer application, and field monitoring for healthy growth.",

    "pod_borer":
    "Small insects attack the cocoa pods and create tiny holes on the surface. "
    "The beans inside become damaged, dry, or undersized. "
    "Affected pods may ripen too early and produce poor-quality cocoa beans.",

    "witches_broom":
    "Too many thin branches grow together, giving the plant a broom-like appearance. "
    "Pods may become abnormal, small, or fail to develop properly. "
    "This disease weakens the cocoa tree and reduces overall cocoa production.",

}

def predict_cocoa_disease(img_path):

    start_time = time.time() # to check model time (start)

    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    pred = model.predict(img_array)[0]

    confidence = round(float(np.max(pred)) * 100 ,2) # model confiden kittan

    top_index = np.argmax(pred)
    label = class_names[top_index]

    end_time=time.time()
    model_time = round((end_time - start_time), 2)

    print("CON & TIME:",confidence,model_time)

    return [
        {
            "disease": label.replace("_", " ").title(),
            "confidence": round(float(pred[top_index]) * 100, 2),
            "treatment": TREATMENTS.get(label, "No treatment available"),
            "impact": IMPACT.get(label, "No impact for your crop"),
            "symptoms": SYMPTOMS.get(label, "Its good!"),
            "confidence":confidence,
            "model_time":model_time,
        }
    ]