# converter.py
from pdf2image import convert_from_path
import tempfile
import os

def convert_pdf_to_images(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.getvalue())
        tmp_file_path = tmp_file.name

    # Convert the PDF to a list of images
    images = convert_from_path(tmp_file_path, poppler_path=r'C:\Users\amitk\Desktop\PLACEMENTS\Zolvit\poppler-24.08.0\Library\bin')
    
    os.unlink(tmp_file_path)  # Delete the temporary file
    
    return images