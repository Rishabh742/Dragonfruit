import streamlit as st
import requests
from PIL import Image
import io

# Initialize session state for images
if 'quality_image' not in st.session_state:
    st.session_state.quality_image = None
if 'maturity_image' not in st.session_state:
    st.session_state.maturity_image = None

def main():
    st.set_page_config(page_title="Dragon Fruit Disease Detection And Maturity Classification")
    st.markdown(
        """
        <link href="styles.css" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title("Navigation")
    options = st.sidebar.radio("Go to", ["Home", "Upload & Train"])

    if options == "Home":
        home()
    elif options == "Upload & Train":
        upload_and_train()

def home():
    st.title("Dragon Fruit Disease Detection And Maturity Classification")
    st.markdown("---")
    st.write("Use the sidebar to navigate to different pages.")
    st.markdown("---")

def upload_and_train():
    st.title("Upload Image and Train Model")
    st.markdown("---")
    st.write("Upload images to start the training process.")
    st.markdown("---")

    col1, col2 = st.columns(2)  # Split the page into two columns

    with col1:
        st.subheader("Quality Grading")
        uploaded_quality_file = st.file_uploader("Choose an image for Quality Grading...", type=["jpg", "jpeg", "png"], key="quality")
        if uploaded_quality_file is not None:
            quality_image = Image.open(uploaded_quality_file)
            st.session_state.quality_image = quality_image
        if st.session_state.quality_image is not None:
            st.image(st.session_state.quality_image, caption='Uploaded Image for Quality Grading.', use_column_width=True)
            st.write("Sending the image to the Flask server for Quality Grading...")

            # Convert PIL image to bytes
            img_byte_arr = io.BytesIO()
            st.session_state.quality_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Send the image to the Flask server
            response = requests.post("http://localhost:5000/quality-grading", files={"file": img_byte_arr})
            result = response.json().get("result", "Error processing the image")
            # Map the result to the appropriate label
            quality_result = "fresh" if result == "1" else "defect"
            st.markdown(f"**Quality Result:** {quality_result}")

    with col2:
        st.subheader("Maturity Detection")
        uploaded_maturity_file = st.file_uploader("Choose an image for Maturity Detection...", type=["jpg", "jpeg", "png"], key="maturity")
        if uploaded_maturity_file is not None:
            maturity_image = Image.open(uploaded_maturity_file)
            st.session_state.maturity_image = maturity_image
        if st.session_state.maturity_image is not None:
            st.image(st.session_state.maturity_image, caption='Uploaded Image for Maturity Detection.', use_column_width=True)
            st.write("Sending the image to the Flask server for Maturity Detection...")

            # Convert PIL image to bytes
            img_byte_arr = io.BytesIO()
            st.session_state.maturity_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Send the image to the Flask server
            response = requests.post("http://localhost:5000/maturity-detection", files={"file": img_byte_arr})
            result = response.json().get("result", "Error processing the image")
            # Map the result to the appropriate label
            maturity_result = "mature" if result == "1" else "immature"
            st.markdown(f"**Maturity Result:** {maturity_result}")

if __name__ == "__main__":
    main()
