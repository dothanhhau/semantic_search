import pytesseract
from pdf2image import convert_from_path
import os
from dotenv import load_dotenv

load_dotenv()

def convert_pdf_to_img(pdf_file_path):
    return convert_from_path(pdf_file_path, poppler_path=str(os.getenv('POPPLER_PDF')))

def convert_image_to_text(file):
    return pytesseract.image_to_string(file, lang='vie')
    
def extract_text(pdf_file_path):
    final_text = ""

    images = convert_pdf_to_img(pdf_file_path)
    for img in images:
        final_text += convert_image_to_text(img)
    return final_text
