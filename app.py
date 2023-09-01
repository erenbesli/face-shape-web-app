import base64

import streamlit as st
import requests

# Define the API endpoints
API_BASE_URL = "http://127.0.0.1:8000"  # Replace with your actual API base URL

# Define the Streamlit app
st.title("Face Recognition App")

# Endpoint 1: Random Celebrities
st.header("Random Celebrities")
option_count = st.slider("Number of Celebrities", min_value=1, max_value=10, value=3)
option_gender = st.selectbox("Gender", ["Male", "Female", "Unspecified"])
option_face_shape = st.selectbox("Face Shape", ["Oval", "Round", "Square", "Heart", "Diamond"])

if st.button("Get Random Celebrities"):
    response = requests.post(
        f"{API_BASE_URL}/celebrity/random",
        json={
            "count": option_count,
            "gender": option_gender.upper(),
            "face_shape": option_face_shape.upper(),
        },
    )
    celebrities = response.json()
    st.write(celebrities)

    for celebrity in celebrities:
        st.write(celebrity["name"])
        st.image(celebrity["image"], caption=celebrity["name"], width=100)

# Endpoint 2: Face Check
st.header("Face Check")
uploaded_image = st.file_uploader("Upload an image for face check", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    if st.button("Check Face"):
        image_contents = uploaded_image.read()
        # Convert the image to base64
        base64_image = base64.b64encode(image_contents).decode()
        response = requests.post(f"{API_BASE_URL}/face/check",
                                 json={"gender": option_gender.upper(),
                                       "image": base64_image})
        result = response.json()
        if "result" in result:
            st.success("Face Detected!")
        else:
            st.error("No Face Detected!")

# Endpoint 3: Face Recommend
st.header("Face Recommend")
uploaded_image = st.file_uploader("Upload an image for face recommendation", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    if st.button("Get Face Recommendation"):

        image_contents = uploaded_image.read()
        # Convert the image to base64
        base64_image = base64.b64encode(image_contents).decode()
        response = requests.post(f"{API_BASE_URL}/face/recommend", json={"gender": option_gender.upper(),
                                                                         "image": base64_image})
        recommendation = response.json()
        # st.write(recommendation)

        recommended_glasses = recommendation["analyze_result"]["recommended_glasses"]
        similar_celebrities = recommendation["analyze_result"]["similar_celebrities"]
        description = recommendation["analyze_result"]["description"]
        face_shape = recommendation["analyze_result"]["face_shape"]

        st.write(description)
        st.write(face_shape)

        for rec in recommended_glasses:
            st.write(rec["model_name"])
            st.image( "http://" + rec["glass_image"], caption=rec["model_name"], width=100)

        for celeb in similar_celebrities:
            st.write(celeb["name"])
            st.image(celeb["image"], caption=celeb["name"], width=100)

# Endpoint 4: Eye Glass Type Prediction
st.header("Eye Glass Type Prediction")
uploaded_image = st.file_uploader("Upload an image for eye glass type prediction", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    if st.button("Predict Eye Glass Type"):
        response = requests.post(f"{API_BASE_URL}/predict/eye-glass-type", files={"image": uploaded_image})
        prediction = response.json()
        for glass_type, confidence in prediction.items():
            st.write(f"Predicted Glass Type: {glass_type}")
            st.write(f"Confidence: {confidence:.2f}")
