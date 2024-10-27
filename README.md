
# Read and Translate Text from Image

This project uses Azure's Vision API to read text from images, translate it to Hindi, and display the translated text on the output image. This tool can be useful for translating text in visual documents or images where text extraction and translation are needed.

## Features
- Extracts text from images using OCR (Optical Character Recognition).
- Translates extracted text from English to Hindi.
- Overlays translated text onto the output image.

## Prerequisites

- **Python 3.7+**
- Azure Vision API credentials for text extraction.
  
### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repository-name.git
   cd your-repository-name
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables for Azure:
   - Create a `.env` file in the root directory and add:
     ```plaintext
     AI_SERVICE_ENDPOINT=your_azure_endpoint
     AI_SERVICE_KEY=your_azure_key
     ```

## Usage

1. Run the script:
   ```bash
   python read-text.py
   ```
2. Follow the on-screen options to select an image and start the translation process.

## Example Output

### Original Image
![Original Image](read-text-translate/images/Marathi.png)

### Translated Image
![Translated Image](read-text-translate/Output/translated_text.jpg)

## Technologies Used

- **Azure Vision API**: For OCR text extraction.
- **Pillow (PIL)**: For image manipulation and drawing.
- **Python-dotenv**: For environment variable management.
