import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Load model once
@st.cache_resource
def load_trained_model():
    return load_model("waste_biodegradable_classifier_fixed.h5")

model = load_trained_model()
img_size = (224, 224)  # same as training

# Prediction function
def predict_uploaded_image(img):
    img = img.resize(img_size)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)[0][0]
    
    # Based on class_indices {'biodegradable': 0, 'non-biodegradable': 1}
    result = "Biodegradable" if prediction < 0.5 else "Non-Biodegradable"
    confidence = prediction if prediction > 0.5 else 1 - prediction
    return result, round(confidence * 100, 2)

# Streamlit UI
st.title("♻️ Waste Classification App")
st.write("Upload an image to classify it as **Biodegradable** or **Non-Biodegradable**.")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert('RGB')
    st.image(img, caption="Uploaded Image", use_column_width=True)

    with st.spinner('Predicting...'):
        label, confidence = predict_uploaded_image(img)
        st.success(f"Prediction: **{label}** ({confidence}% confidence)")
