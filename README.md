**Read and Translate Text from Image**
This project leverages Azure's Vision API to read text from images, translate it, and display the translated text on the output image. It's an ideal solution for scenarios where text extraction and language translation are required for images.

Features
Extract text from any image using OCR.
Translate extracted text from English to Hindi.
Overlay translated text on the output image.
Setup
Prerequisites
Python 3.7+
Azure Vision API credentials for text extraction.
Install dependencies:
bash
Copy code
pip install -r requirements.txt
Environment Variables
Create a .env file in the root directory and add your Azure credentials:

plaintext
Copy code
AI_SERVICE_ENDPOINT=your_azure_endpoint
AI_SERVICE_KEY=your_azure_key
Usage
Run the script:
bash
Copy code
python read-text.py
Select an image from the options provided, and the program will process the image to display translated text.
Example Output
Below are some examples of the input images and their translated outputs.

Original Image
![Marathi](https://github.com/user-attachments/assets/d95ba2e2-7a50-4a0a-9cd0-7f5d853902c4)

Translated Output
![translated_text](https://github.com/user-attachments/assets/e81dd520-0a5f-443a-9592-e098ea169ea4)

Technologies Used
Azure Vision API for text extraction.
Pillow (PIL) for image manipulation.
Python-dotenv to manage environment variables.
