import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(prompt,image):
    model=genai.GenerativeModel('gemini-1.5-flash-latest')
    response=model.generate_content([prompt,image[0]])
    return response.text

def input_image_setup(file):
    if file is not None:
        bytes_data=file.getvalue()

        image_parts=[
            {
                "mime_type": file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title="Calories Counter")
st.header("Calories Counter")
file=st.file_uploader("Upload Image", type=["jpg","jpeg","png"])
image=""
if file is not None:
    image=Image.open(file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

submit=st.button("Tell me about my food")

prompt="""
"You are a nutrition and food analysis expert. I will upload an image of a food dish. Analyze the image and provide the following:
List all identifiable food items present in the dish, line by line.
Estimate the calorie count of each item and the total calories.
Provide a macronutrient breakdown in percentages: carbs, proteins, and fats.
Classify the dish as Healthy or Unhealthy, based on standard dietary guidelines.
Give a clear and concise reason for the classification (e.g., too much sugar, low protein, high trans fats, etc.).
"""

if submit:
    data=input_image_setup(file)
    response=get_response(prompt,data)
    st.subheader("Response:")
    st.write(response)