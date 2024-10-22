# Invoice Data Extraction System

## Understanding the Problem Statement (PS) & Data

**Problem Statement (PS):**
Invoices are an unavoidable part of business operations, from local shops to global companies. However, manual invoice processing is inefficient, prone to errors, and not scalable. The goal here is to build a system that automates the extraction of critical information from invoices, whether they're pristine PDFs, scanned copies, or a combination of both. Our solution will extract meaningful data from any type of invoice document.

### Data:
The variety of invoices we’re working with is diverse and complex:
- **Standard PDFs**: Easier text extraction but requires precision.
- **Scanned PDFs**: Essentially images within PDFs, more challenging to extract data from.
- **Mixed PDFs**: A blend of text and images, difficult for basic extraction methods.

We aim to extract the following key fields:
- Invoice Number
- Invoice Date
- Customer Details
- Line Item Details
- Place of Supply
- Due Date
- Total (including taxes) & Total Discount

---

## Approach Explanation

### Approach:
1. **User Input**: Users upload PDFs or images of invoices.
2. **PDF to Image Conversion**: If the input is a PDF, each page is converted to an image for consistent processing across clean and scanned documents.
3. **Google AI Integration**: Images are processed using **Google's Gemini-1.5-pro-002 model**, which accurately extracts invoice data, regardless of formatting.

### Gemini-1.5-pro-002:
A mid-size multimodal model with a 128,000-token context window, capable of handling up to 384 pages per document. It's optimized for scaling across a wide range of tasks.

---

## Comparison with Other Approaches

### Basic PDF Text Extraction:
- **Tools**: PyPDF2, PDFMiner
- **Pros**: Works well with clean, text-based PDFs.
- **Cons**: Struggles with scanned or mixed-content PDFs. Inefficient for extracting tabular data.

### Optical Character Recognition (OCR):
- **Tools**: Tesseract, Google Cloud Vision
- **Pros**: Effective for scanned documents and various image formats, can handle some non-standard fonts/handwriting.
- **Cons**: Accuracy can vary based on image quality and layout complexity, often requires preprocessing.

### Deep Learning Models (e.g., CRNN):
- **Pros**: High accuracy for complex layouts, learns directly from raw data.
- **Cons**: Requires substantial computational resources, may be overkill for simpler invoices or small-scale tasks.

---

## Code Explanation

### Functions:
- **`get_gemini_response(input, images, prompt)`**: Initializes the Gemini model and generates a response based on the input prompt and images. Returns structured text data.
  
- **`input_image_setup(images)`**: Converts images to a byte format for sending to the Gemini API, preparing them for analysis.
  
- **`validate_invoice_data(response)`**: Validates the model's response, checking for issues such as missing total amounts or mismatches between totals and line items.

---

## Streamlit App Configuration

- **User Interface**: The app allows users to upload multiple PDFs/images and provides a simple interface for handling invoices.
- **Image Display**: Thumbnails of uploaded images are displayed, with the ability to select specific images for detailed viewing.
- **Data Extraction**: Upon submission, the app extracts and validates invoice data, displaying any potential errors or inconsistencies.

### Key Libraries:
- **Pillow (PIL)**: Image processing.
- **Streamlit**: Interactive web application framework.
- **pdf2image**: Converts PDFs to images for easier processing.
- **google.generativeai**: The API used for structured data extraction.

---

## Accuracy Assessment

The system was tested on 41 invoices with varying structures. It consistently extracted the following fields from each PDF:
- **Invoice Number**
- **Invoice Date**
- **Customer Details**
- **Line Item Details**
- **Place of Supply**
- **Due Date**
- **Total (including taxes) & Total Discount**

### Detailed Breakdown:
- **Invoice Number**: 100% accurate across all 41 PDFs.
- **Invoice Date**: Accurate, regardless of formatting or position.
- **Customer Details**: Extracted correctly across diverse formats.
- **Line Item Details**: Captured accurately, even when the number of items varied.
- **Place of Supply**: Extracted successfully in all cases.
- **Due Date**: Always identified correctly.

---

## Error Handling & Reporting

We’ve implemented robust error detection to ensure the accuracy of extracted data. The system flags issues like:
- **Missing or unclear total amounts**.
- **Mismatches between total amounts and line items**.

These validations enhance trust in the system, allowing users to confidently rely on the extracted data.

---

## Data Reliability

In all test cases, the system reliably extracted data, regardless of invoice structure or format. Its ability to adapt to different invoice layouts makes it highly reliable for handling diverse invoice types.

---

## Performance and Cost Analysis

### Trust Determination Logic:
We assign trust scores to each field based on its importance:
- **Invoice Number**: 9
- **Invoice Date**: 9
- **Customer Details**: 9
- **Line Item Details**: 35
- **Place of Supply**: 9
- **Total (incl. taxes & discount)**: 20
- **Due Date**: 9

### Cost-Effectiveness:
Utilizing **Google's Gemini 1.5 API** free tier provides:
- **15 Requests per Minute (RPM)**
- **1 Million Tokens per Minute (TPM)**
- **1,500 Requests per Day (RPD)**

The free tier can handle up to **384 pages** of content per request, making it cost-effective for small to medium businesses. Higher volumes can be managed by upgrading to the paid tier.

### Scalability:
The system scales efficiently, handling large PDFs with minimal latency, making it suitable for both real-time and batch processing.

---

## Instructions To Use

### Setup:
1. Add the **poppler path** to your system's environment variables.
2. Generate a **Google Gemini API key** and add it to the `.env` file.
3. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
4.Install dependencies:pip install -r requirements.txt
5.Run the App: streamlit run app.py
