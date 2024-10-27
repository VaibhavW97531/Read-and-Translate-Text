
from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw, ImageFont
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import requests, uuid, json

# Initialize global variables for Azure clients
cv_client = None

def main():
    load_dotenv()
    setup_azure_clients()
    
    command = input_menu()
    if command in ['1', '2']:
        image_file = select_image_file(command)
        process_image(image_file)

def setup_azure_clients():
    """Authenticate Azure client for Vision service."""
    global cv_client

    ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
    ai_key = os.getenv('AI_SERVICE_KEY')

    cv_client = ImageAnalysisClient(endpoint=ai_endpoint, credential=AzureKeyCredential(ai_key))

def input_menu():
    """Display a menu and get user input for action selection."""
    print('1: Read for image (German.jpg)')
    print('2: Read for image (Marathi.png)')
    return input('Enter a number (or any other key to quit): ')

def select_image_file(command):
    """Select the appropriate image file based on user command."""
    return os.path.join('images', 'German.jpg' if command == '1' else 'Marathi.png')

def process_image(image_file):
    """Analyze the image for text and translate the detected text."""
    print(f'\nProcessing image: {image_file}')
    with open(image_file, "rb") as f:
        image_data = f.read()

    try:
        result = cv_client.analyze(image_data=image_data, visual_features=[VisualFeatures.READ])
        if result.read is not None:
            display_and_translate_text(result.read.blocks, image_file)
        else:
            print("No text found in the image.")
    except Exception as e:
        print("Error analyzing image:", e)

def display_and_translate_text(blocks, image_file):
    """Display the detected text and translate it into specified languages."""
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)
    
    target_languages = ['en']  # Specify target languages here

    for block in blocks:
        for line in block.lines:
            extracted_text = line.text
            print(f"  Original Text: {extracted_text}")

            translated_texts = translate_text(extracted_text, target_languages)
            for lang, translated_text in zip(target_languages, translated_texts):
                print(f"  Translated Text ({lang}): {translated_text}")

            draw_bounding_box(draw, line.bounding_polygon, ', '.join(translated_texts))

    outputfile = 'Output/translated_text.jpg'
    image.save(outputfile)
    print(f'\n  Results saved in {outputfile}')

def translate_text(text, target_languages):
    """Translate the given text to the specified target languages using Azure Translator API."""
    key = os.getenv('TRANSLATOR_SERVICE_KEY')
    endpoint = os.getenv('TRANSLATOR_SERVICE_ENDPOINT').rstrip('/')
    location = os.getenv('TRANSLATOR_SERVICE_REGION')

    # Debugging: Ensure credentials and endpoint are loaded correctly
    if not key or not endpoint or not location:
        print("Error: Missing API key, endpoint, or region in environment variables.")
        return [text] * len(target_languages)

    path = '/translate'
    constructed_url = f"{endpoint}{path}"

    params = {
        'api-version': '3.0',
        'to': target_languages
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]

    try:
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        response.raise_for_status()  # Ensure request was successful

        response_json = response.json()
        
        if 'translations' in response_json[0]:
            return [translation['text'] for translation in response_json[0]['translations']]
        else:
            print("Error: Translation data missing in response.")
            return [text] * len(target_languages)

    except requests.exceptions.RequestException as e:
        print(f"Translation error: {e}")
        return [text] * len(target_languages)


def draw_bounding_box(draw, bounding_polygon, translated_text):
    """Draw a filled polygon to hide the original text and add the translated text within it."""
    # Calculate the width and height of the bounding box
    bounding_coords = [(point.x, point.y) for point in bounding_polygon]
    min_x = min(coord[0] for coord in bounding_coords)
    max_x = max(coord[0] for coord in bounding_coords)
    min_y = min(coord[1] for coord in bounding_coords)
    max_y = max(coord[1] for coord in bounding_coords)

    # Determine the size of the bounding box
    box_width = max_x - min_x
    box_height = max_y - min_y

    # Set a base font size and calculate the scale based on the box height
    base_font_size = 100  # Adjust this value if needed
    font_size = int(box_height * 0.75)  # Use 75% of the bounding box height for font size

    # Make sure the font size doesn't exceed the base font size
    font_size = min(font_size, base_font_size)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Draw a filled polygon to cover the original text
    draw.polygon(bounding_coords, fill='white')  # Set fill color to cover original text

    # Position for text (adjust slightly for padding)
    x = min_x + 5
    y = min_y + 5
    draw.text((x, y), translated_text, fill='black', font=font)  # Display translated text in black




if __name__ == "__main__":
    main()
