import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
# import pandas as pd
# import numpy as np
import io
from converter import convert_pdf_to_images

load_dotenv()

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, images, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-002')
    response = model.generate_content([input, *images, prompt])
    return response.text

def input_image_setup(images):
    image_parts = []
    for img in images:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        image_parts.append({
            "mime_type": "image/png",
            "data": buffered.getvalue()
        })
    return image_parts
def validate_invoice_data(response):
    # Convert the response to lowercase for easier checking
    response_lower = response.lower()
    
    issues = []
    
    # Check for missing invoice number
    # if "invoice number" not in response_lower or "invoice no" not in response_lower:
    #     issues.append("Invoice number might be missing")
    
    # Check for unclear total amount
    if "total amount" not in response_lower and "total" not in response_lower:
        issues.append("Total amount might be unclear")
    
    # Basic check for mismatch between total and line items
    if "total" in response_lower and "line item" in response_lower:
        # This is a very basic check and might need refinement
        total_index = response_lower.index("total")
        line_items_index = response_lower.index("line item")
        if total_index < line_items_index:
            issues.append("Potential mismatch between total and line items")
    
    return issues

st.set_page_config(page_title="Zolvit InvoXT Demo")

st.header("Zolvit InvoXT Application")
input = st.text_input("Input Prompt: ", key="input")
uploaded_files = st.file_uploader("Choose PDF or images...", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True)

MAX_DEFAULT_IMAGES = 3

images = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            pdf_images = convert_pdf_to_images(uploaded_file)
            images.extend(pdf_images)
        else:
            image = Image.open(uploaded_file)
            images.append(image)

    st.subheader("Select Images to View")
    cols = st.columns(5)  # Create 5 columns for a row of thumbnails
    selected_images = []
    for i, img in enumerate(images):
        with cols[i % 5]:
            thumbnail = img.copy()
            thumbnail.thumbnail((100, 100))
            default_checked = i < MAX_DEFAULT_IMAGES
            if st.checkbox(f"Image {i+1}", value=default_checked, key=f"checkbox_{i}"):
                selected_images.append(i)
            st.image(thumbnail, use_column_width=True)

    if selected_images:
        st.subheader("Selected Images")
        for i in selected_images:
            st.image(images[i], caption=f"Image {i+1}", use_column_width=True)

submit = st.button("Tell me about the images")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input images
               """
if submit and images:
    image_data = input_image_setup(images)
    response = get_gemini_response(input_prompt, image_data, input)
    
    # Perform validation checks
    issues = validate_invoice_data(response)
    
    st.subheader("The Response is")
    st.write(response)
    
    # Display any issues found
    if issues:
        st.subheader("Potential Issues Detected")
        for issue in issues:
            st.warning(issue)
        st.warning("Please review the extracted data carefully.")
    else:
        st.success("No potential issues detected in the extraction.")
elif submit:
    st.warning("Please upload at least one PDF or image before submitting.")