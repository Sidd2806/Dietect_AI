from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini prompt
input_prompt = """
You are an expert nutritionist. When shown an image of food, analyze it to:

1. List each food item with its estimated calorie count.
2. Create a table with all food items and their calories.
3. If the user uploads vegetables or ingredients and asks for a recipe, do a Google search and return a high-nutrition recipe suggestion.

Answer clearly and in structured format.
"""

# Streamlit page setup
st.set_page_config(
    page_title="🍽️ AI Nutritionist",
    page_icon="🍎",
    layout="centered",
)

st.title("🍽️ AI Nutritionist")
st.markdown("Analyze your food and get a complete nutritional breakdown & recipe suggestions using AI!")

st.divider()

# User input
input = st.text_input("📝 Enter your question or context:", placeholder="e.g., What’s in my plate and how many calories does it have?", key="input")

uploaded_file = st.file_uploader("📤 Upload a food image (JPG, PNG, JPEG):", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Image", use_container_width=True)
else:
    st.info("Please upload an image to begin.")

# Submit Button
submit = st.button("🧠 Analyze Image and Predict Calories")

# Helper function to convert uploaded file to Gemini format
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Get Gemini response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# On submit
if submit and uploaded_file is not None:
    with st.spinner("Analyzing image and generating response..."):
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input, image_data, input_prompt)
    
    st.divider()
    st.subheader("🧾 AI Nutritionist's Report")
    # st.code(response, language='markdown')  # cleaner formatting
    st.write(response)
    st.success("✅ Analysis complete!")
elif submit and uploaded_file is None:
    st.error("❌ Please upload an image before submitting.")
