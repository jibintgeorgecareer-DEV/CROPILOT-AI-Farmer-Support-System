import numpy as np
import tensorflow as tf
import time
from tensorflow.keras.preprocessing import image

model = tf.keras.models.load_model(
    "croppilot_app/ml_models/plant_disease_model.h5"
)

class_names = [
    "Potato_Early_blight",
    "Potato_Late_blight",
    "Potato_healthy",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_healthy"
]

TREATMENTS = {

    "Potato_Early_blight":
    "Remove infected leaves and keep the field clean to reduce disease spread. "
    "Rotate crops regularly instead of planting potatoes in the same soil every season. "
    "Applying recommended fungicides such as mancozeb or chlorothalonil can help protect healthy plants.",

    "Potato_Late_blight":
    "Remove and destroy infected potato plants immediately to prevent the disease from spreading rapidly. "
    "Use disease-resistant potato varieties whenever possible and avoid excessive moisture in the field. "
    "Preventive fungicide sprays like mancozeb or cymoxanil mixtures can help protect the crop.",

    "Potato_healthy":
    "Your potato plant appears healthy and no treatment is needed at the moment. "
    "Continue proper watering, fertilizer application, and regular field monitoring to maintain healthy growth.",

    "Tomato_Early_blight":
    "Remove infected leaves and avoid keeping the soil too wet around the plant. "
    "Prune lower leaves and improve airflow between plants to reduce fungal growth. "
    "Copper fungicides or chlorothalonil sprays may help protect healthy tomato plants.",

    "Tomato_Late_blight":
    "Remove infected tomato plants quickly before the disease spreads to nearby crops. "
    "Avoid overhead watering and keep leaves as dry as possible. "
    "Protect healthy plants using suitable fungicides such as copper-based sprays or mancozeb.",

    "Tomato_healthy":
    "Your tomato plant looks healthy and no disease treatment is currently required. "
    "Continue regular care, proper watering, and nutrient management for better growth and production.",

}

IMPACT = {

    "Potato_Early_blight":
    "This disease weakens potato plants and reduces the size and quality of the tubers. "
    "If the infection spreads heavily, farmers may experience lower crop yield and reduced market value.",

    "Potato_Late_blight":
    "Late blight is a very dangerous potato disease that can spread rapidly during cool and wet weather. "
    "It can destroy large areas of potato cultivation in a short time and cause severe production loss if not controlled early.",

    "Potato_healthy":
    "No harmful disease impact detected on the potato crop. "
    "The plants appear healthy and capable of good growth and production under proper care.",

    "Tomato_Early_blight":
    "This disease weakens tomato plants and reduces both fruit quality and overall yield. "
    "Infected plants may produce fewer healthy tomatoes and show poor growth over time.",

    "Tomato_Late_blight":
    "Tomato late blight spreads very quickly in rainy and cool conditions. "
    "If not managed early, it can destroy tomato plants rapidly and lead to major crop loss for farmers.",

    "Tomato_healthy":
    "No disease impact detected on the tomato crop. "
    "The plants look healthy and suitable for normal growth and fruit production.",

}

SYMPTOMS = {

    "Potato_Early_blight":
    "Dark brown spots appear on older potato leaves, usually with ring-like patterns in the center. "
    "Leaves may turn yellow, dry up, and fall early, making the plant weak and unhealthy.",

    "Potato_Late_blight":
    "Leaves develop wet-looking brown or black patches that spread quickly during cool and rainy weather. "
    "White fungal growth may appear under the leaves, and potato tubers can develop dark rotten areas inside and outside.",

    "Potato_healthy":
    "No major disease symptoms detected on the potato plant. "
    "Leaves and stems appear healthy and normal.",

    "Tomato_Early_blight":
    "Brown circular spots appear on lower tomato leaves, often with ring-like patterns. "
    "Leaves may dry and fall early, and dark damaged spots can appear near the top of the tomato fruit.",

    "Tomato_Late_blight":
    "Large wet-looking brown patches appear on tomato leaves and spread rapidly in humid weather. "
    "White fungus-like growth may appear under the leaves, and fruits can develop soft brown rotten areas.",

    "Tomato_healthy":
    "No disease symptoms detected on the tomato plant. "
    "The plant looks healthy with normal leaves and fruits.",

}


def predict_disease(img_path):

    start_time = time.time() # to check model time (start)

    img = image.load_img(img_path, target_size=(224,224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    pred = model.predict(img_array)[0]

    confidence = round(float(np.max(pred)) * 100 ,2) # model confiden kittan

    top_index = np.argmax(pred)
    raw_label = class_names[top_index]
    label=class_names[top_index].replace("_"," ")

    end_time=time.time()
    model_time = round((end_time - start_time), 2)


    return [
        {
            "disease": label,
            "confidence": confidence,
            "model_time": model_time,
            "treatment": TREATMENTS.get(raw_label, "Consult Agriculture Officer"),
            "impact": IMPACT.get(raw_label, "NO IMPACTS"),
            "symptoms": SYMPTOMS.get(raw_label, "NO SYMPTOMS"),
            
        }
    ]   