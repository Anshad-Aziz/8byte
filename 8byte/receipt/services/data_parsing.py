import re
from datetime import datetime
from PIL import Image
import pytesseract
import PyPDF2
from typing import Dict
import logging
import os

# Set up logging
logger = logging.getLogger(__name__)

# Explicitly set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def parse_file(full_file_path: str) -> Dict:
    try:
        logger.info(f"Parsing file: {full_file_path}")
        if not os.path.exists(full_file_path):
            logger.error(f"File does not exist: {full_file_path}")
            raise FileNotFoundError(f"File does not exist: {full_file_path}")

        file_ext = os.path.splitext(full_file_path)[1].lower()
        
        if file_ext in ['.jpg', '.png']:
            return parse_image(full_file_path)
        elif file_ext == '.pdf':
            return parse_pdf(full_file_path)
        elif file_ext == '.txt':
            return parse_text(full_file_path)
        else:
            logger.error(f"Unsupported file extension: {file_ext}")
            raise ValueError(f"Unsupported file extension: {file_ext}")

    except Exception as e:
        logger.error(f"Error parsing file {full_file_path}: {str(e)}", exc_info=True)
        raise Exception(f"Error parsing file: {str(e)}")

def parse_image(full_file_path: str) -> Dict:
    try:
        logger.info(f"Processing image: {full_file_path}")
        text = pytesseract.image_to_string(Image.open(full_file_path))
        logger.debug(f"Extracted text: {text[:200]}...")  # Log first 200 chars
        return extract_data(text, full_file_path)
    except Exception as e:
        logger.error(f"Error processing image {full_file_path}: {str(e)}", exc_info=True)
        raise

def parse_pdf(full_file_path: str) -> Dict:
    try:
        logger.info(f"Processing PDF: {full_file_path}")
        with open(full_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + '\n'
            logger.debug(f"Extracted text: {text[:200]}...")  # Log first 200 chars
        return extract_data(text, full_file_path)
    except Exception as e:
        logger.error(f"Error processing PDF {full_file_path}: {str(e)}", exc_info=True)
        raise

def parse_text(full_file_path: str) -> Dict:
    try:
        logger.info(f"Processing text file: {full_file_path}")
        with open(full_file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        logger.debug(f"Extracted text: {text[:200]}...")  # Log first 200 chars
        return extract_data(text, full_file_path)
    except Exception as e:
        logger.error(f"Error processing text file {full_file_path}: {str(e)}", exc_info=True)
        raise

def extract_data(text: str, full_file_path: str) -> Dict:
    try:
        logger.info("Extracting data from text")
        vendor_patterns = [r'(Walmart|Amazon|Target|Verizon|Comcast)', r'Store:?\s*([^\n]+)']
        date_patterns = [r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', r'(?:\d{1,2}\s)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}']
        amount_patterns = [r'\$\d+\.\d{2}', r'Total:?\s*\$?\d+\.\d{2}']
        
        vendor = 'Unknown'
        date = None
        amount = 0.0

        # Extract vendor
        for pattern in vendor_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                vendor = match.group(1)
                logger.info(f"Found vendor: {vendor}")
                break

        # Extract date
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    date = datetime.strptime(match.group(0), '%m/%d/%Y').date()
                    logger.info(f"Found date: {date}")
                    break
                except:
                    try:
                        date = datetime.strptime(match.group(0), '%m-%d-%Y').date()
                        logger.info(f"Found date: {date}")
                        break
                    except:
                        continue

        # Extract amount
        for pattern in amount_patterns:
            match = re.search(pattern, text)
            if match:
                amount = float(match.group(0).replace('$', '').replace('Total:', '').strip())
                logger.info(f"Found amount: {amount}")
                break

        result = {
            'vendor': vendor,
            'transaction_date': date or datetime.now().date(),
            'amount': amount,
            'category': categorize_vendor(vendor),
            'file_name': full_file_path
        }
        logger.info(f"Extracted data: {result}")
        return result

    except Exception as e:
        logger.error(f"Error extracting data: {str(e)}", exc_info=True)
        raise

def categorize_vendor(vendor: str) -> str:
    categories = {
        'Walmart': 'Groceries',
        'Amazon': 'Online Shopping',
        'Target': 'Retail',
        'Verizon': 'Utilities',
        'Comcast': 'Utilities'
    }
    return categories.get(vendor, 'Uncategorized')