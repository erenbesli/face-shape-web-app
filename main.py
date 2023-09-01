# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import streamlit as st
    import requests

    # Define the API endpoints
    API_BASE_URL = "http://your-api-base-url"  # Replace with your actual API base URL

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
                "gender": option_gender.lower(),
                "face_shape": option_face_shape.lower(),
            },
        )
        celebrities = response.json()
        st.write(celebrities)

    # Endpoint 2: Face Check
    st.header("Face Check")
    uploaded_image = st.file_uploader("Upload an image for face check", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        if st.button("Check Face"):
            response = requests.post(f"{API_BASE_URL}/face/check", files={"image": uploaded_image})
            result = response.json()
            if result["result"]:
                st.success("Face Detected!")
            else:
                st.error("No Face Detected!")

    # Endpoint 3: Face Recommend
    st.header("Face Recommend")
    uploaded_image = st.file_uploader("Upload an image for face recommendation", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        if st.button("Get Face Recommendation"):
            response = requests.post(f"{API_BASE_URL}/face/recommend", files={"image": uploaded_image})
            recommendation = response.json()
            st.write(recommendation)

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

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
